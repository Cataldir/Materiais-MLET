"""Validacao local inspirada em Great Expectations.

Demonstra como aplicar expectativas declarativas a dados tabulares,
usando o conceito de suites e checkpoints do Great Expectations sem
exigir a instalacao da biblioteca.

Conceitos-chave
---------------
- **Expectation Suite**: conjunto nomeado de regras de qualidade.
- **Checkpoint**: execucao de uma suite sobre um dataset.
- **Expectativa declarativa**: regra expressa como especificacao, nao como
  codigo imperativo.
- **Fallback local**: mesma semantica quando a biblioteca nao esta disponivel.

Referencia:
    Great Expectations — https://docs.greatexpectations.io/

Uso:
    python ge_validation.py
"""

from __future__ import annotations

import json
import logging
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 24


# ---------------------------------------------------------------------------
# 1. Tipos e estruturas de dados
# ---------------------------------------------------------------------------


class ExpectationKind(str, Enum):
    """Categorias de expectativas suportadas pelo validador local."""

    MIN = "min"
    MAX = "max"
    BETWEEN = "between"
    SET = "set"
    MISSING = "missing"
    UNIQUE = "unique"
    NOT_NULL = "not_null"


@dataclass(frozen=True, slots=True)
class ExpectationSpec:
    """Especificacao declarativa de uma regra de qualidade.

    Cada expectativa descreve UMA restricao sobre UMA coluna.
    O formato e inspirado nas expectations do Great Expectations:

    - ``name``: identificador unico da regra.
    - ``column``: coluna alvo no DataFrame.
    - ``kind``: tipo de check (min, max, between, set, missing, unique, not_null).
    - ``threshold``: valor de referencia (depende do kind).
    - ``description``: descricao legivel para relatorios.
    """

    name: str
    column: str
    kind: ExpectationKind
    threshold: float | tuple[float, float] | tuple[str, ...] | None = None
    description: str = ""


@dataclass(frozen=True, slots=True)
class ExpectationResult:
    """Resultado de uma expectativa individual."""

    name: str
    success: bool
    observed_value: float | str
    description: str = ""


@dataclass(frozen=True, slots=True)
class CheckpointResult:
    """Resultado consolidado do checkpoint local."""

    backend: str
    dataset_name: str
    success: bool
    results: tuple[ExpectationResult, ...]
    timestamp: str = ""
    total_expectations: int = 0
    passed_expectations: int = 0
    failed_expectations: int = 0


# ---------------------------------------------------------------------------
# 2. Deteccao do Great Expectations
# ---------------------------------------------------------------------------


def load_gx_module():
    """Carrega Great Expectations apenas se estiver disponivel."""
    try:
        import great_expectations as gx  # noqa: F401
    except ImportError:
        return None
    return gx


# ---------------------------------------------------------------------------
# 3. Definicao de suites de expectativa
# ---------------------------------------------------------------------------


def build_churn_suite() -> tuple[ExpectationSpec, ...]:
    """Suite de expectativas para um dataset de churn de telecom.

    Cobre completude, faixa de valores, categorias permitidas e unicidade.
    Essa suite representa o que uma equipe de dados definiria para validar
    lotes de entrada antes de alimentar um modelo de predicao de churn.
    """
    return (
        ExpectationSpec(
            "tenure_not_null", "tenure", ExpectationKind.NOT_NULL,
            description="Coluna tenure deve estar preenchida",
        ),
        ExpectationSpec(
            "missing_monthly_charges_low", "monthly_charges",
            ExpectationKind.MISSING, 0.05,
            description="Maximo 5 porcento de valores ausentes em monthly_charges",
        ),
        ExpectationSpec(
            "tenure_non_negative", "tenure", ExpectationKind.MIN, 0.0,
            description="Tenure nao pode ser negativo",
        ),
        ExpectationSpec(
            "tenure_max_reasonable", "tenure", ExpectationKind.MAX, 120.0,
            description="Tenure maximo razoavel: 10 anos",
        ),
        ExpectationSpec(
            "monthly_charges_range", "monthly_charges",
            ExpectationKind.BETWEEN, (0.0, 500.0),
            description="Cobranca mensal entre 0 e 500",
        ),
        ExpectationSpec(
            "total_charges_non_negative", "total_charges",
            ExpectationKind.MIN, 0.0,
            description="Total de cobrancas nao pode ser negativo",
        ),
        ExpectationSpec(
            "contract_type_valid", "contract",
            ExpectationKind.SET, ("month-to-month", "one_year", "two_year"),
            description="Tipo de contrato deve ser um dos valores aceitos",
        ),
        ExpectationSpec(
            "churn_label_binary", "churn",
            ExpectationKind.SET, ("yes", "no"),
            description="Label de churn deve ser binaria",
        ),
        ExpectationSpec(
            "customer_id_unique", "customer_id",
            ExpectationKind.UNIQUE,
            description="IDs de clientes devem ser unicos",
        ),
    )


def build_basic_titanic_suite() -> tuple[ExpectationSpec, ...]:
    """Suite basica para o dataset Titanic (comparacao didatica)."""
    return (
        ExpectationSpec(
            "fare_non_negative", "fare", ExpectationKind.MIN, 0.0,
            description="Tarifa nao pode ser negativa",
        ),
        ExpectationSpec(
            "age_between", "age", ExpectationKind.BETWEEN, (0.0, 95.0),
            description="Idade deve estar entre 0 e 95",
        ),
        ExpectationSpec(
            "segment_known", "segment",
            ExpectationKind.SET, ("basic", "plus", "vip"),
            description="Segmento deve ser um dos valores definidos",
        ),
        ExpectationSpec(
            "missing_name_low", "name", ExpectationKind.MISSING, 0.10,
            description="Maximo 10 porcento de nomes ausentes",
        ),
    )


# ---------------------------------------------------------------------------
# 4. Motor de avaliacao local
# ---------------------------------------------------------------------------


def evaluate_spec(df: pd.DataFrame, spec: ExpectationSpec) -> ExpectationResult:
    """Avalia uma expectativa declarativa sem dependencia externa.

    Cada ``kind`` mapeia para uma logica de check especifica:

    - ``min`` / ``max``: valor minimo/maximo da coluna.
    - ``between``: min e max devem estar no intervalo.
    - ``set``: todos os valores devem pertencer ao conjunto.
    - ``missing``: taxa de nulos menor que o threshold.
    - ``unique``: nao deve haver duplicatas na coluna.
    - ``not_null``: coluna nao deve ter nenhum nulo.
    """
    series = df[spec.column]
    observed_value: float | str

    if spec.kind == ExpectationKind.MIN:
        minimum = float(series.min())
        success = minimum >= float(spec.threshold)
        observed_value = minimum

    elif spec.kind == ExpectationKind.MAX:
        maximum = float(series.max())
        success = maximum <= float(spec.threshold)
        observed_value = maximum

    elif spec.kind == ExpectationKind.BETWEEN:
        lower, upper = spec.threshold
        min_value, max_value = float(series.min()), float(series.max())
        success = min_value >= float(lower) and max_value <= float(upper)
        observed_value = f"{min_value:.2f}:{max_value:.2f}"

    elif spec.kind == ExpectationKind.SET:
        allowed = set(spec.threshold)
        invalid_values = sorted(set(series.dropna().astype(str)) - allowed)
        success = not invalid_values
        observed_value = ",".join(invalid_values) if invalid_values else "ok"

    elif spec.kind == ExpectationKind.MISSING:
        missing_rate = float(series.isna().mean())
        success = missing_rate <= float(spec.threshold)
        observed_value = round(missing_rate, 4)

    elif spec.kind == ExpectationKind.UNIQUE:
        duplicate_count = int(series.dropna().duplicated().sum())
        success = duplicate_count == 0
        observed_value = f"{duplicate_count} duplicatas"

    elif spec.kind == ExpectationKind.NOT_NULL:
        null_count = int(series.isna().sum())
        success = null_count == 0
        observed_value = f"{null_count} nulos"

    else:
        raise ValueError(f"Tipo de expectativa nao suportado: {spec.kind}")

    return ExpectationResult(
        name=spec.name,
        success=success,
        observed_value=observed_value,
        description=spec.description,
    )


# ---------------------------------------------------------------------------
# 5. Checkpoint — execucao completa de uma suite
# ---------------------------------------------------------------------------


def run_checkpoint(
    dataset_name: str,
    df: pd.DataFrame,
    suite: tuple[ExpectationSpec, ...] | None = None,
) -> CheckpointResult:
    """Executa um checkpoint local ou compativel com GX.

    Um checkpoint e a unidade de execucao: aplica todas as expectativas
    de uma suite sobre um dataset e consolida o resultado.
    """
    if suite is None:
        suite = build_basic_titanic_suite()

    backend = "great_expectations" if load_gx_module() is not None else "local"
    results = tuple(evaluate_spec(df, spec) for spec in suite)
    passed = sum(1 for r in results if r.success)

    return CheckpointResult(
        backend=backend,
        dataset_name=dataset_name,
        success=all(r.success for r in results),
        results=results,
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        total_expectations=len(results),
        passed_expectations=passed,
        failed_expectations=len(results) - passed,
    )


# ---------------------------------------------------------------------------
# 6. Datasets sinteticos
# ---------------------------------------------------------------------------


def build_churn_examples(
    random_state: int = RANDOM_STATE,
    rows: int = 200,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera datasets de churn sinteticos (valido e invalido)."""
    rng = np.random.default_rng(random_state)

    valid = pd.DataFrame({
        "customer_id": [f"CUST-{i:04d}" for i in range(rows)],
        "tenure": rng.integers(0, 72, size=rows),
        "monthly_charges": rng.normal(65, 20, size=rows).round(2).clip(18, 120),
        "total_charges": rng.normal(2000, 800, size=rows).round(2).clip(0, 8000),
        "contract": rng.choice(
            ["month-to-month", "one_year", "two_year"],
            size=rows, p=[0.5, 0.25, 0.25],
        ),
        "churn": rng.choice(["yes", "no"], size=rows, p=[0.27, 0.73]),
    })

    invalid = valid.copy()
    invalid.loc[0, "tenure"] = -5
    invalid.loc[1, "tenure"] = 200
    invalid.loc[2, "monthly_charges"] = 999.99
    invalid.loc[3, "monthly_charges"] = -10.0
    invalid.loc[4, "total_charges"] = -500.0
    invalid.loc[5, "contract"] = "quarterly"
    invalid.loc[7, "churn"] = "maybe"
    invalid.loc[8, "customer_id"] = invalid.loc[0, "customer_id"]
    invalid.loc[10:14, "tenure"] = None
    invalid.loc[15:30, "monthly_charges"] = None
    return valid, invalid


def build_titanic_examples(
    random_state: int = RANDOM_STATE,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera exemplos Titanic para compatibilidade com a versao anterior."""
    rng = np.random.default_rng(random_state)
    valid = pd.DataFrame({
        "name": [f"cliente_{i}" for i in range(18)],
        "age": rng.integers(18, 76, size=18),
        "fare": rng.normal(85, 22, size=18).round(2).clip(10, 180),
        "segment": rng.choice(["basic", "plus", "vip"], size=18, p=[0.5, 0.35, 0.15]),
    })
    invalid = valid.copy()
    invalid.loc[0, "fare"] = -15.0
    invalid.loc[1, "age"] = 132
    invalid.loc[2, "segment"] = "unknown"
    invalid.loc[3:6, "name"] = None
    return valid, invalid


# ---------------------------------------------------------------------------
# 7. Relatorio de resultados
# ---------------------------------------------------------------------------


def format_checkpoint_report(result: CheckpointResult) -> str:
    """Formata o resultado de um checkpoint como texto legivel."""
    lines = [
        f"\n{'=' * 60}",
        f"CHECKPOINT: {result.dataset_name}",
        f"Backend: {result.backend}",
        f"Timestamp: {result.timestamp}",
        f"Resultado: {'APROVADO' if result.success else 'REPROVADO'}",
        f"Expectativas: {result.passed_expectations}/{result.total_expectations} aprovadas",
        f"{'-' * 60}",
    ]
    for r in result.results:
        status = "pass" if r.success else "FAIL"
        lines.append(f"  [{status}] {r.name}: {r.observed_value}")
        if r.description:
            lines.append(f"         {r.description}")
    lines.append(f"{'=' * 60}\n")
    return "\n".join(lines)


def export_checkpoint_json(
    result: CheckpointResult,
    output_path: Path | None = None,
) -> dict[str, Any]:
    """Exporta resultado do checkpoint como JSON (para integracao com CI/CD)."""
    data = {
        "backend": result.backend,
        "dataset_name": result.dataset_name,
        "success": result.success,
        "timestamp": result.timestamp,
        "summary": {
            "total": result.total_expectations,
            "passed": result.passed_expectations,
            "failed": result.failed_expectations,
        },
        "results": [asdict(r) for r in result.results],
    }
    if output_path is not None:
        output_path.write_text(json.dumps(data, indent=2, ensure_ascii=False))
        LOGGER.info("Relatorio exportado para %s", output_path)
    return data


# ---------------------------------------------------------------------------
# 8. Demo principal
# ---------------------------------------------------------------------------


def run_ge_validation_demo() -> dict[str, CheckpointResult]:
    """Executa os datasets de exemplo com ambas as suites."""
    valid_titanic, invalid_titanic = build_titanic_examples()
    titanic_suite = build_basic_titanic_suite()

    valid_churn, invalid_churn = build_churn_examples()
    churn_suite = build_churn_suite()

    return {
        "titanic_valid": run_checkpoint("titanic_valid", valid_titanic, titanic_suite),
        "titanic_invalid": run_checkpoint("titanic_invalid", invalid_titanic, titanic_suite),
        "churn_valid": run_checkpoint("churn_valid", valid_churn, churn_suite),
        "churn_invalid": run_checkpoint("churn_invalid", invalid_churn, churn_suite),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    results = run_ge_validation_demo()
    for checkpoint in results.values():
        LOGGER.info(format_checkpoint_report(checkpoint))
    total = len(results)
    passed = sum(1 for r in results.values() if r.success)
    LOGGER.info("Resumo: %d/%d checkpoints aprovados", passed, total)


if __name__ == "__main__":
    main()
