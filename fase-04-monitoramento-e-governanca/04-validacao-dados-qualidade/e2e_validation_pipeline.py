"""Solucao end-to-end: pipeline de validacao de dados para ML.

Integra os quatro pilares de validacao das aulas anteriores em uma
pipeline completa e auto-contida:

1. Expectativas declarativas (conceitos do Great Expectations — Aula 01)
2. Schema tipado para DataFrames (conceitos do Pandera — Aula 02)
3. Validacao runtime de payloads (conceitos do Pydantic — Aula 03)
4. Quality gate com decisao pass/warn/fail (conceitos da Aula 04)

A pipeline simula o ciclo completo de um sistema de ML em producao:

    Ingestao → Validacao de Entrada → Treinamento → Validacao de Saida
    → Serving → Validacao Runtime → Gate Final

Todos os conceitos estao reimplementados aqui para que o script seja
executavel independentemente das outras aulas.

Uso:
    python e2e_validation_pipeline.py
"""

from __future__ import annotations

import json
import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Protocol

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42


# ===================================================================
# PARTE 1 — EXPECTATIVAS DECLARATIVAS (conceitos da Aula 01)
# ===================================================================


class ExpectationKind(str, Enum):
    """Categorias de expectativas suportadas."""

    MIN = "min"
    MAX = "max"
    BETWEEN = "between"
    SET = "set"
    MISSING = "missing"
    UNIQUE = "unique"
    NOT_NULL = "not_null"


@dataclass(frozen=True, slots=True)
class ExpectationSpec:
    """Regra declarativa de qualidade sobre uma coluna."""

    name: str
    column: str
    kind: ExpectationKind
    threshold: float | tuple[float, float] | tuple[str, ...] | None = None
    description: str = ""


@dataclass(frozen=True, slots=True)
class ExpectationResult:
    """Resultado de uma expectativa."""

    name: str
    success: bool
    observed: str


def evaluate_expectation(df: pd.DataFrame, spec: ExpectationSpec) -> ExpectationResult:
    """Avalia uma expectativa declarativa sobre um DataFrame."""
    series = df[spec.column]

    if spec.kind == ExpectationKind.MIN:
        val = float(series.min())
        return ExpectationResult(spec.name, val >= float(spec.threshold), f"{val:.2f}")

    if spec.kind == ExpectationKind.MAX:
        val = float(series.max())
        return ExpectationResult(spec.name, val <= float(spec.threshold), f"{val:.2f}")

    if spec.kind == ExpectationKind.BETWEEN:
        lo, hi = spec.threshold
        mn, mx = float(series.min()), float(series.max())
        return ExpectationResult(spec.name, mn >= float(lo) and mx <= float(hi), f"{mn:.2f}:{mx:.2f}")

    if spec.kind == ExpectationKind.SET:
        allowed = set(spec.threshold)
        bad = sorted(set(series.dropna().astype(str)) - allowed)
        return ExpectationResult(spec.name, not bad, ",".join(bad) or "ok")

    if spec.kind == ExpectationKind.MISSING:
        rate = float(series.isna().mean())
        return ExpectationResult(spec.name, rate <= float(spec.threshold), f"{rate:.4f}")

    if spec.kind == ExpectationKind.UNIQUE:
        dups = int(series.dropna().duplicated().sum())
        return ExpectationResult(spec.name, dups == 0, f"{dups} duplicatas")

    if spec.kind == ExpectationKind.NOT_NULL:
        nulls = int(series.isna().sum())
        return ExpectationResult(spec.name, nulls == 0, f"{nulls} nulos")

    raise ValueError(f"Kind desconhecido: {spec.kind}")


def build_churn_expectations() -> tuple[ExpectationSpec, ...]:
    """Suite de expectativas para dados de churn."""
    return (
        ExpectationSpec("tenure_not_null", "tenure", ExpectationKind.NOT_NULL),
        ExpectationSpec("tenure_min", "tenure", ExpectationKind.MIN, 0.0),
        ExpectationSpec("tenure_max", "tenure", ExpectationKind.MAX, 120.0),
        ExpectationSpec("charges_range", "monthly_charges", ExpectationKind.BETWEEN, (0.0, 500.0)),
        ExpectationSpec("charges_missing", "monthly_charges", ExpectationKind.MISSING, 0.05),
        ExpectationSpec("total_non_neg", "total_charges", ExpectationKind.MIN, 0.0),
        ExpectationSpec("contract_set", "contract", ExpectationKind.SET,
                        ("month-to-month", "one_year", "two_year")),
        ExpectationSpec("churn_binary", "churn", ExpectationKind.SET, ("yes", "no")),
        ExpectationSpec("id_unique", "customer_id", ExpectationKind.UNIQUE),
    )


def run_expectation_suite(name: str, df: pd.DataFrame) -> dict[str, Any]:
    """Executa suite de expectativas e retorna resultado consolidado."""
    results = [evaluate_expectation(df, spec) for spec in build_churn_expectations()]
    passed = sum(1 for r in results if r.success)
    return {
        "stage": "expectation_suite",
        "dataset": name,
        "passed": passed == len(results),
        "total": len(results),
        "ok": passed,
        "fail": len(results) - passed,
        "failures": [r.name for r in results if not r.success],
    }


# ===================================================================
# PARTE 2 — SCHEMA TIPADO (conceitos da Aula 02)
# ===================================================================


def load_pandera():
    """Carrega Pandera se disponivel."""
    try:
        import pandera.pandas as pa
        return pa
    except ImportError:
        try:
            import pandera as pa
            return pa
        except ImportError:
            return None


def validate_input_schema(df: pd.DataFrame) -> dict[str, Any]:
    """Valida o DataFrame de entrada usando Pandera (ou fallback local)."""
    pa = load_pandera()

    if pa is not None:
        schema = pa.DataFrameSchema(
            columns={
                "customer_id": pa.Column(str, nullable=False),
                "tenure": pa.Column(float, checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(120),
                ], nullable=False),
                "monthly_charges": pa.Column(float, checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(500),
                ], nullable=True),
                "total_charges": pa.Column(float, checks=[
                    pa.Check.greater_than_or_equal_to(0),
                ], nullable=True),
                "contract": pa.Column(str, checks=[
                    pa.Check.isin(["month-to-month", "one_year", "two_year"]),
                ], nullable=False),
                "churn": pa.Column(str, checks=[
                    pa.Check.isin(["yes", "no"]),
                ], nullable=False),
            },
            coerce=True,
        )
        try:
            schema.validate(df, lazy=True)
            return {"stage": "input_schema", "passed": True, "backend": "pandera", "errors": []}
        except Exception as exc:
            return {"stage": "input_schema", "passed": False, "backend": "pandera", "errors": [str(exc)]}
    else:
        # Fallback local
        errors = []
        for col in ["customer_id", "tenure", "monthly_charges", "total_charges", "contract", "churn"]:
            if col not in df.columns:
                errors.append(f"coluna ausente: {col}")
        if df["tenure"].min() < 0:
            errors.append("tenure negativo")
        if df["monthly_charges"].dropna().min() < 0:
            errors.append("monthly_charges negativo")
        return {"stage": "input_schema", "passed": not errors, "backend": "local", "errors": errors}


def validate_prediction_schema(predictions: pd.DataFrame) -> dict[str, Any]:
    """Valida predicoes do modelo."""
    pa = load_pandera()

    if pa is not None:
        schema = pa.DataFrameSchema(
            columns={
                "customer_id": pa.Column(str, nullable=False),
                "prediction": pa.Column(int, checks=[pa.Check.isin([0, 1])]),
                "probability": pa.Column(float, checks=[
                    pa.Check.greater_than_or_equal_to(0.0),
                    pa.Check.less_than_or_equal_to(1.0),
                ]),
                "model_version": pa.Column(str, nullable=False),
            },
        )
        try:
            schema.validate(predictions, lazy=True)
            return {"stage": "prediction_schema", "passed": True, "backend": "pandera", "errors": []}
        except Exception as exc:
            return {"stage": "prediction_schema", "passed": False, "backend": "pandera", "errors": [str(exc)]}
    else:
        errors = []
        if predictions["probability"].min() < 0 or predictions["probability"].max() > 1:
            errors.append("probabilidade fora de [0, 1]")
        return {"stage": "prediction_schema", "passed": not errors, "backend": "local", "errors": errors}


# ===================================================================
# PARTE 3 — VALIDACAO RUNTIME (conceitos da Aula 03)
# ===================================================================


class SchemaStrategy(Protocol):
    """Contrato para validacao estrutural."""

    name: str

    def validate(self, payload: dict[str, Any]) -> list[str]: ...


class LocalStrategy:
    """Validador local sem dependencias."""

    name = "local"

    def validate(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        required = {"customer_id": str, "age": int, "monthly_spend": (int, float),
                     "prediction_horizon_days": int}
        for f, t in required.items():
            if f not in payload:
                errors.append(f"missing:{f}")
            elif not isinstance(payload[f], t):
                errors.append(f"type:{f}")
        return errors


class PydanticStrategy(LocalStrategy):
    """Valida com Pydantic quando disponivel."""

    name = "pydantic"

    def validate(self, payload: dict[str, Any]) -> list[str]:
        from pydantic import BaseModel, Field, ValidationError

        class Payload(BaseModel):
            customer_id: str = Field(min_length=1)
            age: int = Field(ge=0, le=150)
            monthly_spend: float = Field(ge=0)
            prediction_horizon_days: int = Field(ge=1, le=365)
            segment: str | None = None

        try:
            Payload(**payload)
        except ValidationError as exc:
            return [f"pydantic:{'.'.join(map(str, e['loc']))}" for e in exc.errors()]
        return []


class BusinessValidator(ABC):
    """Chain of Responsibility para regras de negocio."""

    def __init__(self) -> None:
        self._next: BusinessValidator | None = None

    def set_next(self, h: BusinessValidator) -> BusinessValidator:
        self._next = h
        return h

    def handle(self, p: dict[str, Any]) -> list[str]:
        errs = self.check(p)
        if self._next:
            errs.extend(self._next.handle(p))
        return errs

    @abstractmethod
    def check(self, p: dict[str, Any]) -> list[str]: ...


class RangeValidator(BusinessValidator):
    def check(self, p: dict[str, Any]) -> list[str]:
        errs: list[str] = []
        if isinstance(p.get("age"), int) and not 18 <= p["age"] <= 100:
            errs.append("range:age")
        if isinstance(p.get("monthly_spend"), (int, float)) and float(p["monthly_spend"]) < 0:
            errs.append("range:monthly_spend")
        return errs


class SegmentValidator(BusinessValidator):
    def check(self, p: dict[str, Any]) -> list[str]:
        seg = p.get("segment")
        if seg and seg not in {"basic", "plus", "vip"}:
            return ["business:segment"]
        return []


def select_strategy() -> SchemaStrategy:
    try:
        import pydantic  # noqa: F401
        return PydanticStrategy()
    except ImportError:
        return LocalStrategy()


def build_chain() -> BusinessValidator:
    first = RangeValidator()
    first.set_next(SegmentValidator())
    return first


def validate_serving_payloads(payloads: list[dict[str, Any]]) -> dict[str, Any]:
    """Valida batch de payloads de serving."""
    strategy = select_strategy()
    chain = build_chain()

    accepted, rejected_details = 0, []
    for i, p in enumerate(payloads):
        errs = strategy.validate(p) + chain.handle(p)
        if not errs:
            accepted += 1
        else:
            rejected_details.append({"index": i, "errors": errs})

    total = len(payloads)
    rate = accepted / total if total else 0
    return {
        "stage": "runtime_validation",
        "passed": rate >= 0.80,
        "backend": strategy.name,
        "total": total,
        "accepted": accepted,
        "rejected": total - accepted,
        "acceptance_rate": round(rate, 4),
        "rejected_details": rejected_details[:5],
    }


# ===================================================================
# PARTE 4 — QUALITY GATE (conceitos da Aula 04)
# ===================================================================


@dataclass(frozen=True, slots=True)
class GateThresholds:
    missing_warn: float = 0.03
    missing_fail: float = 0.10
    duplicate_warn: float = 0.02
    duplicate_fail: float = 0.08
    range_warn: float = 0.03
    range_fail: float = 0.08


def classify(value: float, warn: float, fail: float) -> str:
    if value >= fail:
        return "fail"
    if value >= warn:
        return "warn"
    return "pass"


def run_quality_gate(df: pd.DataFrame, thresholds: GateThresholds | None = None) -> dict[str, Any]:
    """Executa quality gate sobre o dataset."""
    t = thresholds or GateThresholds()
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    missing = float(df[numeric_cols].isna().mean().mean()) if numeric_cols else 0
    dupes = float(df.duplicated().mean())

    # Range violations para colunas numericas
    violations = 0
    if "tenure" in df.columns:
        violations += int((df["tenure"].notna() & ~df["tenure"].between(0, 120)).sum())
    if "monthly_charges" in df.columns:
        violations += int((df["monthly_charges"].notna() & ~df["monthly_charges"].between(0, 500)).sum())
    range_rate = violations / len(df) if len(df) else 0

    checks = {
        "missing": {"value": round(missing, 4), "status": classify(missing, t.missing_warn, t.missing_fail)},
        "duplicates": {"value": round(dupes, 4), "status": classify(dupes, t.duplicate_warn, t.duplicate_fail)},
        "range": {"value": round(range_rate, 4), "status": classify(range_rate, t.range_warn, t.range_fail)},
    }

    warnings = [k for k, v in checks.items() if v["status"] == "warn"]
    failures = [k for k, v in checks.items() if v["status"] == "fail"]
    decision = "fail" if failures else ("warn" if warnings else "pass")

    return {
        "stage": "quality_gate",
        "passed": decision != "fail",
        "decision": decision,
        "checks": checks,
        "warnings": warnings,
        "failures": failures,
    }


# ===================================================================
# PARTE 5 — GERACAO DE DADOS SINTETICOS
# ===================================================================


def generate_churn_dataset(
    rows: int = 500,
    random_state: int = RANDOM_STATE,
    inject_errors: bool = False,
) -> pd.DataFrame:
    """Gera dataset de churn sintetico.

    Com ``inject_errors=True``, simula problemas realistas:
    valores ausentes, fora de faixa, duplicatas e categorias invalidas.
    """
    rng = np.random.default_rng(random_state)
    df = pd.DataFrame({
        "customer_id": [f"CUST-{i:05d}" for i in range(rows)],
        "tenure": rng.integers(0, 72, size=rows).astype(float),
        "monthly_charges": rng.normal(65, 20, size=rows).round(2).clip(18, 120),
        "total_charges": rng.normal(2000, 800, size=rows).round(2).clip(0, 8000),
        "contract": rng.choice(
            ["month-to-month", "one_year", "two_year"], size=rows, p=[0.5, 0.25, 0.25],
        ),
        "churn": rng.choice(["yes", "no"], size=rows, p=[0.27, 0.73]),
    })

    if inject_errors:
        idx = rng.choice(rows, size=int(rows * 0.05), replace=False)
        df.loc[idx[:3], "tenure"] = [-1, -5, 200]
        df.loc[idx[3:6], "monthly_charges"] = [np.nan, np.nan, -50]
        df.loc[idx[6:8], "contract"] = ["quarterly", "unknown"]
        df.loc[idx[8:10], "churn"] = ["maybe", ""]
        df = pd.concat([df, df.iloc[:3]], ignore_index=True)

    return df


def simulate_predictions(df: pd.DataFrame, random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """Simula predicoes de churn baseadas em heuristicas."""
    rng = np.random.default_rng(random_state)
    tenure_norm = df["tenure"].fillna(0) / 72
    charges_norm = df["monthly_charges"].fillna(65) / 120
    prob = np.clip(0.3 - 0.2 * tenure_norm + 0.15 * charges_norm + rng.normal(0, 0.1, len(df)), 0.01, 0.99)
    return pd.DataFrame({
        "customer_id": df["customer_id"],
        "prediction": (prob > 0.5).astype(int),
        "probability": prob.round(4),
        "model_version": "v2.1.0",
    })


def build_serving_payloads(df: pd.DataFrame, n: int = 10, random_state: int = RANDOM_STATE) -> list[dict[str, Any]]:
    """Cria payloads de serving (validos e invalidos)."""
    rng = np.random.default_rng(random_state)
    payloads = []
    for _ in range(n):
        row = df.iloc[rng.integers(0, len(df))]
        payloads.append({
            "customer_id": str(row["customer_id"]),
            "age": int(rng.integers(20, 70)),
            "monthly_spend": float(row["monthly_charges"]),
            "prediction_horizon_days": int(rng.integers(7, 60)),
            "segment": rng.choice(["basic", "plus", "vip"]),
        })
    # Payloads invalidos
    payloads.append({"customer_id": "", "age": 15, "monthly_spend": -100,
                     "prediction_horizon_days": 200, "segment": "unknown"})
    payloads.append({"customer_id": "C-999", "age": "velho", "monthly_spend": 50,
                     "prediction_horizon_days": 30})
    return payloads


# ===================================================================
# PARTE 6 — ORQUESTRADOR DA PIPELINE
# ===================================================================


@dataclass
class PipelineReport:
    """Relatorio completo da pipeline."""

    timestamp: str
    mode: str
    stages: list[dict[str, Any]]
    overall: str
    passed: int
    failed: int


def run_pipeline(inject_errors: bool = False, random_state: int = RANDOM_STATE) -> PipelineReport:
    """Executa a pipeline completa de validacao end-to-end."""
    logger.info("=" * 70)
    logger.info("PIPELINE E2E — %s", "ERROS INJETADOS" if inject_errors else "DADOS LIMPOS")
    logger.info("=" * 70)

    df = generate_churn_dataset(rows=500, random_state=random_state, inject_errors=inject_errors)
    logger.info("Dataset: %d linhas x %d colunas", *df.shape)

    stages: list[dict[str, Any]] = []

    # Estagio 1: Expectation Suite
    logger.info("\n[1/5] Expectation Suite...")
    s1 = run_expectation_suite("churn_input", df)
    stages.append(s1)
    logger.info("       %s — %d/%d expectativas", "PASS" if s1["passed"] else "FAIL", s1["ok"], s1["total"])

    # Estagio 2: Input Schema
    logger.info("[2/5] Input Schema Validation...")
    s2 = validate_input_schema(df)
    stages.append(s2)
    logger.info("       %s (backend=%s)", "PASS" if s2["passed"] else "FAIL", s2["backend"])

    # Estagio 3: Prediction Schema
    logger.info("[3/5] Prediction Schema Validation...")
    preds = simulate_predictions(df, random_state=random_state)
    s3 = validate_prediction_schema(preds)
    stages.append(s3)
    logger.info("       %s (backend=%s)", "PASS" if s3["passed"] else "FAIL", s3["backend"])

    # Estagio 4: Runtime Validation
    logger.info("[4/5] Runtime Payload Validation...")
    payloads = build_serving_payloads(df, n=10, random_state=random_state)
    s4 = validate_serving_payloads(payloads)
    stages.append(s4)
    logger.info("       %s — %d/%d aceitos (%.0f%%)", "PASS" if s4["passed"] else "FAIL",
                s4["accepted"], s4["total"], s4["acceptance_rate"] * 100)

    # Estagio 5: Quality Gate
    logger.info("[5/5] Quality Gate...")
    s5 = run_quality_gate(df)
    stages.append(s5)
    logger.info("       %s — decisao=%s", "PASS" if s5["passed"] else "FAIL", s5["decision"])

    passed = sum(1 for s in stages if s["passed"])
    failed = len(stages) - passed
    overall = "APPROVED" if failed == 0 else ("WARNINGS" if failed <= 2 else "REJECTED")

    return PipelineReport(
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        mode="errors_injected" if inject_errors else "clean",
        stages=stages,
        overall=overall,
        passed=passed,
        failed=failed,
    )


def format_report(report: PipelineReport) -> str:
    """Formata relatorio da pipeline."""
    lines = [
        f"\n{'=' * 70}",
        f"RELATORIO — {report.mode.upper()}",
        f"{'=' * 70}",
        f"Timestamp: {report.timestamp}",
        f"Resultado: {report.overall}",
        f"Estagios: {report.passed}/{report.passed + report.failed} aprovados",
        f"{'-' * 70}",
    ]
    for s in report.stages:
        status = "PASS" if s["passed"] else "FAIL"
        lines.append(f"  [{status}] {s['stage']}")
    lines.append(f"{'=' * 70}\n")
    return "\n".join(lines)


# ===================================================================
# PONTO DE ENTRADA
# ===================================================================


def main() -> None:
    # Cenario 1: dados limpos
    report_clean = run_pipeline(inject_errors=False)
    logger.info(format_report(report_clean))

    # Cenario 2: dados com erros
    report_dirty = run_pipeline(inject_errors=True, random_state=99)
    logger.info(format_report(report_dirty))

    # Comparacao
    logger.info("--- Comparacao Final ---")
    logger.info("Limpo: %s (%d/%d)", report_clean.overall, report_clean.passed, report_clean.passed + report_clean.failed)
    logger.info("Sujo:  %s (%d/%d)", report_dirty.overall, report_dirty.passed, report_dirty.passed + report_dirty.failed)


if __name__ == "__main__":
    main()
