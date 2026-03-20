"""Validacao local inspirada em Great Expectations."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 24


@dataclass(frozen=True, slots=True)
class ExpectationSpec:
    """Especificacao declarativa de uma regra de qualidade."""

    name: str
    column: str
    kind: str
    threshold: float | tuple[float, float] | tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ExpectationResult:
    """Resultado de uma expectativa individual."""

    name: str
    success: bool
    observed_value: float | str


@dataclass(frozen=True, slots=True)
class CheckpointResult:
    """Resultado consolidado do checkpoint local."""

    backend: str
    dataset_name: str
    success: bool
    results: tuple[ExpectationResult, ...]


def load_gx_module():
    """Carrega Great Expectations apenas se estiver disponivel."""

    try:
        import great_expectations as gx
    except ImportError:
        return None
    return gx


def build_expectation_suite() -> tuple[ExpectationSpec, ...]:
    """Define a suite de expectativas da aula."""

    return (
        ExpectationSpec("fare_non_negative", "fare", "min", 0.0),
        ExpectationSpec("age_between", "age", "between", (0.0, 95.0)),
        ExpectationSpec("segment_known", "segment", "set", ("basic", "plus", "vip")),
        ExpectationSpec("missing_name_low", "name", "missing", 0.10),
    )


def build_examples(random_state: int = RANDOM_STATE) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera exemplos validos e invalidos para o checkpoint."""

    rng = np.random.default_rng(random_state)
    valid = pd.DataFrame(
        {
            "name": [f"cliente_{index}" for index in range(18)],
            "age": rng.integers(18, 76, size=18),
            "fare": rng.normal(85, 22, size=18).round(2).clip(10, 180),
            "segment": rng.choice(["basic", "plus", "vip"], size=18, p=[0.5, 0.35, 0.15]),
        }
    )
    invalid = valid.copy()
    invalid.loc[0, "fare"] = -15.0
    invalid.loc[1, "age"] = 132
    invalid.loc[2, "segment"] = "unknown"
    invalid.loc[3:6, "name"] = None
    return valid, invalid


def evaluate_spec(df: pd.DataFrame, spec: ExpectationSpec) -> ExpectationResult:
    """Avalia uma expectativa declarativa sem dependencia externa."""

    series = df[spec.column]
    if spec.kind == "min":
        minimum = float(series.min())
        success = minimum >= float(spec.threshold)
        observed_value: float | str = minimum
    elif spec.kind == "between":
        lower, upper = spec.threshold
        min_value = float(series.min())
        max_value = float(series.max())
        success = min_value >= float(lower) and max_value <= float(upper)
        observed_value = f"{min_value:.1f}:{max_value:.1f}"
    elif spec.kind == "set":
        allowed = set(spec.threshold)
        invalid_values = sorted(set(series.dropna().astype(str)) - allowed)
        success = not invalid_values
        observed_value = ",".join(invalid_values) if invalid_values else "ok"
    elif spec.kind == "missing":
        missing_rate = float(series.isna().mean())
        success = missing_rate <= float(spec.threshold)
        observed_value = missing_rate
    else:
        raise ValueError(f"Unsupported expectation kind: {spec.kind}")
    return ExpectationResult(name=spec.name, success=success, observed_value=observed_value)


def run_checkpoint(dataset_name: str, df: pd.DataFrame) -> CheckpointResult:
    """Executa um checkpoint local ou compatível com GX."""

    backend = "great_expectations" if load_gx_module() is not None else "local"
    results = tuple(evaluate_spec(df, spec) for spec in build_expectation_suite())
    success = all(result.success for result in results)
    return CheckpointResult(
        backend=backend,
        dataset_name=dataset_name,
        success=success,
        results=results,
    )


def run_ge_validation_demo() -> dict[str, CheckpointResult]:
    """Executa os dois datasets de exemplo."""

    valid, invalid = build_examples()
    return {
        "valid": run_checkpoint("valid", valid),
        "invalid": run_checkpoint("invalid", invalid),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    results = run_ge_validation_demo()
    for name, checkpoint in results.items():
        LOGGER.info("dataset=%s backend=%s success=%s", name, checkpoint.backend, checkpoint.success)
        for result in checkpoint.results:
            LOGGER.info("  %s -> success=%s observed=%s", result.name, result.success, result.observed_value)


if __name__ == "__main__":
    main()