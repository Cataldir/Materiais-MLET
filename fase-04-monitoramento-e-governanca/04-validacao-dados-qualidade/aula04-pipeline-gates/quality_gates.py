"""Pipeline local de gates de qualidade para dados tabulares.

Executa checks leves sobre datasets sinteticos e decide se cada lote deve
passar, seguir com aviso ou falhar antes das proximas etapas.

Uso:
    python quality_gates.py
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
DATASET_ROWS = 60
DEFAULT_THRESHOLDS = None


@dataclass(frozen=True, slots=True)
class GateThresholds:
    """Thresholds usados para classificar um lote."""

    missing_warn: float = 0.03
    missing_fail: float = 0.10
    duplicate_warn: float = 0.02
    duplicate_fail: float = 0.08
    range_warn: float = 0.03
    range_fail: float = 0.08


@dataclass(frozen=True, slots=True)
class CheckResult:
    """Resultado de um check individual."""

    name: str
    value: float
    status: str


@dataclass(frozen=True, slots=True)
class QualityDecision:
    """Resultado final do gate para um dataset."""

    dataset_name: str
    decision: str
    checks: list[CheckResult]
    warning_checks: list[str]
    failing_checks: list[str]


def build_sample_datasets(random_state: int = RANDOM_STATE) -> dict[str, pd.DataFrame]:
    """Gera datasets sinteticos para os tres resultados do gate."""
    rng = np.random.default_rng(random_state)
    base = pd.DataFrame(
        {
            "customer_id": np.arange(1, DATASET_ROWS + 1, dtype=int),
            "age": rng.integers(21, 70, size=DATASET_ROWS),
            "monthly_spend": rng.normal(180, 30, size=DATASET_ROWS).round(2),
            "churn_score": rng.uniform(0.1, 0.9, size=DATASET_ROWS).round(3),
        }
    )

    pass_candidate = base.copy()

    warn_candidate = base.copy()
    warn_candidate.loc[[3, 7], "monthly_spend"] = np.nan
    warn_candidate.loc[[10, 11], "age"] = [19, 91]

    fail_candidate = pd.concat([base.iloc[:8], base.copy()], ignore_index=True)
    fail_candidate.loc[:9, "monthly_spend"] = np.nan
    fail_candidate.loc[[12, 14, 16, 18, 20, 22], "age"] = [15, 95, 14, 97, 13, 99]
    fail_candidate.loc[[13, 17, 21, 25, 29], "monthly_spend"] = [
        -50,
        -10,
        900,
        -25,
        850,
    ]

    return {
        "pass_candidate": pass_candidate,
        "warn_candidate": warn_candidate,
        "fail_candidate": fail_candidate,
    }


def classify_rate(value: float, warn_threshold: float, fail_threshold: float) -> str:
    """Converte uma taxa em status de gate."""
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
    spend_invalid = dataset["monthly_spend"].notna() & ~dataset[
        "monthly_spend"
    ].between(0, 500)
    churn_invalid = dataset["churn_score"].notna() & ~dataset["churn_score"].between(
        0, 1
    )
    violations = age_invalid | spend_invalid | churn_invalid
    return float(violations.mean())


def evaluate_quality_gate(
    dataset_name: str,
    dataset: pd.DataFrame,
    thresholds: GateThresholds,
) -> QualityDecision:
    """Avalia um dataset e decide o gate final."""
    checks = [
        CheckResult(
            name="missing_rate",
            value=compute_missing_rate(dataset),
            status=classify_rate(
                compute_missing_rate(dataset),
                thresholds.missing_warn,
                thresholds.missing_fail,
            ),
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
    ]
    warning_checks = [check.name for check in checks if check.status == "warn"]
    failing_checks = [check.name for check in checks if check.status == "fail"]

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
    )


def run_quality_gate_pipeline(
    random_state: int = RANDOM_STATE,
    thresholds: GateThresholds | None = DEFAULT_THRESHOLDS,
) -> list[QualityDecision]:
    """Executa o fluxo fixo da aula para tres lotes sinteticos."""
    # Template Method via sequencia fixa: gerar lotes -> validar -> decidir -> resumir.
    active_thresholds = thresholds or GateThresholds()
    datasets = build_sample_datasets(random_state=random_state)
    decisions = [
        evaluate_quality_gate(name, dataset, active_thresholds)
        for name, dataset in datasets.items()
    ]
    for decision in decisions:
        logger.info(
            "%s | decision=%s | warnings=%s | failing=%s",
            decision.dataset_name,
            decision.decision,
            decision.warning_checks,
            decision.failing_checks,
        )
    return decisions


if __name__ == "__main__":
    run_quality_gate_pipeline()
