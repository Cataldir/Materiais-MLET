"""Pipeline local de gates de qualidade para dados tabulares.

Executa checks leves sobre datasets sinteticos e decide se cada lote
deve passar, seguir com aviso ou falhar antes das proximas etapas.

Conceitos-chave
---------------
- **Quality Gate**: ponto de decisao binaria/ternaria em uma pipeline.
- **Pass / Warn / Fail**: tres estados possiveis de um gate.
- **Threshold configuravel**: limites de tolerancia para cada check.
- **Composicao de checks**: missing, duplicatas, faixa e consistencia.
- **Template Method**: sequencia fixa (gerar → validar → decidir → resumir).

Uso:
    python quality_gates.py
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
DATASET_ROWS = 60


# ---------------------------------------------------------------------------
# 1. Configuracao de thresholds
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class GateThresholds:
    """Thresholds configuráveis para classificar um lote.

    Cada par (warn, fail) define dois limites:
    - abaixo de warn → pass
    - entre warn e fail → warn (lote liberado com ressalvas)
    - acima de fail → fail (lote bloqueado)
    """

    missing_warn: float = 0.03
    missing_fail: float = 0.10
    duplicate_warn: float = 0.02
    duplicate_fail: float = 0.08
    range_warn: float = 0.03
    range_fail: float = 0.08
    schema_warn: float = 0.01
    schema_fail: float = 0.05


# ---------------------------------------------------------------------------
# 2. Estruturas de resultado
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Resultado de um check individual."""

    name: str
    value: float
    status: str
    detail: str = ""


@dataclass(frozen=True, slots=True)
class QualityDecision:
    """Resultado final do gate para um dataset."""

    dataset_name: str
    decision: str
    checks: list[CheckResult]
    warning_checks: list[str]
    failing_checks: list[str]
    timestamp: str = ""
    row_count: int = 0


# ---------------------------------------------------------------------------
# 3. Datasets sinteticos
# ---------------------------------------------------------------------------


def build_sample_datasets(random_state: int = RANDOM_STATE) -> dict[str, pd.DataFrame]:
    """Gera datasets sinteticos para os tres resultados do gate.

    - ``pass_candidate``: lote limpo, sem problemas.
    - ``warn_candidate``: lote com poucos problemas (passa com ressalvas).
    - ``fail_candidate``: lote com muitos problemas (bloqueado).
    """
    rng = np.random.default_rng(random_state)

    base = pd.DataFrame({
        "customer_id": np.arange(1, DATASET_ROWS + 1, dtype=int),
        "age": rng.integers(21, 70, size=DATASET_ROWS),
        "monthly_spend": rng.normal(180, 30, size=DATASET_ROWS).round(2),
        "churn_score": rng.uniform(0.1, 0.9, size=DATASET_ROWS).round(3),
    })

    # Lote limpo
    pass_candidate = base.copy()

    # Lote com warnings
    warn_candidate = base.copy()
    warn_candidate.loc[[3, 7], "monthly_spend"] = np.nan
    warn_candidate.loc[[10, 11], "age"] = [19, 91]

    # Lote com falhas
    fail_candidate = pd.concat([base.iloc[:8], base.copy()], ignore_index=True)
    fail_candidate.loc[:9, "monthly_spend"] = np.nan
    fail_candidate.loc[[12, 14, 16, 18, 20, 22], "age"] = [15, 95, 14, 97, 13, 99]
    fail_candidate.loc[[13, 17, 21, 25, 29], "monthly_spend"] = [-50, -10, 900, -25, 850]

    return {
        "pass_candidate": pass_candidate,
        "warn_candidate": warn_candidate,
        "fail_candidate": fail_candidate,
    }


# ---------------------------------------------------------------------------
# 4. Funcoes de check
# ---------------------------------------------------------------------------


def classify_rate(value: float, warn_threshold: float, fail_threshold: float) -> str:
    """Converte uma taxa em status de gate (pass, warn, fail)."""
    if value >= fail_threshold:
        return "fail"
    if value >= warn_threshold:
        return "warn"
    return "pass"


def compute_missing_rate(dataset: pd.DataFrame) -> float:
    """Calcula taxa de valores ausentes nas colunas criticas."""
    critical_columns = ["age", "monthly_spend", "churn_score"]
    return float(dataset[critical_columns].isna().mean().mean())


def compute_duplicate_rate(dataset: pd.DataFrame) -> float:
    """Calcula taxa de linhas duplicadas completas."""
    return float(dataset.duplicated().mean())


def compute_range_violation_rate(dataset: pd.DataFrame) -> float:
    """Calcula taxa de violacoes de faixa em colunas numericas."""
    age_invalid = dataset["age"].notna() & ~dataset["age"].between(21, 90)
    spend_invalid = dataset["monthly_spend"].notna() & ~dataset["monthly_spend"].between(0, 500)
    churn_invalid = dataset["churn_score"].notna() & ~dataset["churn_score"].between(0, 1)
    violations = age_invalid | spend_invalid | churn_invalid
    return float(violations.mean())


def compute_schema_violation_rate(dataset: pd.DataFrame) -> float:
    """Verifica se colunas criticas tem tipos corretos."""
    numeric_columns = ["age", "monthly_spend", "churn_score"]
    violations = 0
    for col in numeric_columns:
        non_numeric = pd.to_numeric(dataset[col], errors="coerce").isna() & dataset[col].notna()
        violations += int(non_numeric.sum())
    return violations / (len(dataset) * len(numeric_columns))


# ---------------------------------------------------------------------------
# 5. Motor de decisao do gate
# ---------------------------------------------------------------------------


def evaluate_quality_gate(
    dataset_name: str,
    dataset: pd.DataFrame,
    thresholds: GateThresholds,
) -> QualityDecision:
    """Avalia um dataset e decide o gate final.

    A decisao segue a regra mais restritiva:
    - se qualquer check e ``fail``, o gate e ``fail``.
    - se qualquer check e ``warn`` (e nenhum e ``fail``), gate e ``warn``.
    - senao, gate e ``pass``.
    """
    checks = [
        CheckResult(
            name="missing_rate",
            value=compute_missing_rate(dataset),
            status=classify_rate(
                compute_missing_rate(dataset),
                thresholds.missing_warn,
                thresholds.missing_fail,
            ),
            detail=f"colunas criticas: {['age', 'monthly_spend', 'churn_score']}",
        ),
        CheckResult(
            name="duplicate_rate",
            value=compute_duplicate_rate(dataset),
            status=classify_rate(
                compute_duplicate_rate(dataset),
                thresholds.duplicate_warn,
                thresholds.duplicate_fail,
            ),
        ),
        CheckResult(
            name="range_violation_rate",
            value=compute_range_violation_rate(dataset),
            status=classify_rate(
                compute_range_violation_rate(dataset),
                thresholds.range_warn,
                thresholds.range_fail,
            ),
        ),
        CheckResult(
            name="schema_violation_rate",
            value=compute_schema_violation_rate(dataset),
            status=classify_rate(
                compute_schema_violation_rate(dataset),
                thresholds.schema_warn,
                thresholds.schema_fail,
            ),
        ),
    ]

    warning_checks = [c.name for c in checks if c.status == "warn"]
    failing_checks = [c.name for c in checks if c.status == "fail"]

    if failing_checks:
        decision = "fail"
    elif warning_checks:
        decision = "warn"
    else:
        decision = "pass"

    return QualityDecision(
        dataset_name=dataset_name,
        decision=decision,
        checks=checks,
        warning_checks=warning_checks,
        failing_checks=failing_checks,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        row_count=len(dataset),
    )


# ---------------------------------------------------------------------------
# 6. Relatorio
# ---------------------------------------------------------------------------


def format_gate_report(decision: QualityDecision) -> str:
    """Formata decisao do gate como texto legivel."""
    status_icon = {"pass": "PASS", "warn": "WARN", "fail": "FAIL"}
    lines = [
        f"\n{'=' * 60}",
        f"GATE: {decision.dataset_name} | {status_icon[decision.decision]}",
        f"Linhas: {decision.row_count} | Timestamp: {decision.timestamp}",
        f"{'-' * 60}",
    ]
    for check in decision.checks:
        lines.append(f"  [{check.status.upper():4s}] {check.name}: {check.value:.4f}")
    if decision.warning_checks:
        lines.append(f"  Warnings: {decision.warning_checks}")
    if decision.failing_checks:
        lines.append(f"  Failures: {decision.failing_checks}")
    lines.append(f"{'=' * 60}")
    return "\n".join(lines)


def export_gate_report(
    decisions: list[QualityDecision],
    output_path: Path | None = None,
) -> list[dict[str, Any]]:
    """Exporta resultados como JSON."""
    data = []
    for d in decisions:
        data.append({
            "dataset": d.dataset_name,
            "decision": d.decision,
            "timestamp": d.timestamp,
            "row_count": d.row_count,
            "checks": [
                {"name": c.name, "value": c.value, "status": c.status}
                for c in d.checks
            ],
            "warnings": d.warning_checks,
            "failures": d.failing_checks,
        })
    if output_path is not None:
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
    return data


# ---------------------------------------------------------------------------
# 7. Pipeline principal
# ---------------------------------------------------------------------------


def run_quality_gate_pipeline(
    random_state: int = RANDOM_STATE,
    thresholds: GateThresholds | None = None,
) -> list[QualityDecision]:
    """Executa o fluxo fixo da aula para tres lotes sinteticos.

    Template Method: gerar lotes → validar → decidir → resumir.
    """
    active_thresholds = thresholds or GateThresholds()
    datasets = build_sample_datasets(random_state=random_state)

    decisions = [
        evaluate_quality_gate(name, dataset, active_thresholds)
        for name, dataset in datasets.items()
    ]

    for decision in decisions:
        logger.info(format_gate_report(decision))

    # Resumo
    counts = {"pass": 0, "warn": 0, "fail": 0}
    for d in decisions:
        counts[d.decision] += 1
    logger.info(
        "\nResumo: %d pass, %d warn, %d fail de %d lotes",
        counts["pass"], counts["warn"], counts["fail"], len(decisions),
    )
    return decisions


if __name__ == "__main__":
    run_quality_gate_pipeline()
