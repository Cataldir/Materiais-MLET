"""Drift Simulator — simulação de diferentes tipos de drift para demonstração.

Demonstra data drift, concept drift e label drift com visualizações
e exemplos práticos usando datasets sintéticos.

Uso:
    python drift_simulator.py
"""

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
N_REFERENCE = 1000
N_PRODUCTION = 500


@dataclass
class DriftScenario:
    """Representa um cenário de drift com dados de referência e produção.

    Attributes:
        name: Nome do cenário.
        description: Descrição do tipo de drift.
        reference_data: Dados de referência (treino).
        production_data: Dados de produção (inferência).
        reference_labels: Labels de referência (opcional).
        production_labels: Labels de produção (opcional).
    """

    name: str
    description: str
    reference_data: pd.DataFrame
    production_data: pd.DataFrame
    reference_labels: pd.Series | None = None
    production_labels: pd.Series | None = None


@dataclass
class DriftSummary:
    """Resume um cenario com metricas leves e deterministicas."""

    name: str
    description: str
    feature_ks: dict[str, float]
    drifted_features: list[str]
    mean_shifts: dict[str, float]
    label_rate_delta: float | None = None


def simulate_data_drift(rng: np.random.Generator) -> DriftScenario:
    """Simula data drift: mudança na distribuição das features de entrada.

    Args:
        rng: Gerador de números aleatórios.

    Returns:
        Cenário de data drift.
    """
    reference = pd.DataFrame(
        {
            "age": rng.normal(35, 10, N_REFERENCE).clip(18, 80),
            "income": rng.lognormal(10, 0.5, N_REFERENCE),
            "credit_score": rng.normal(650, 80, N_REFERENCE).clip(300, 850),
        }
    )
    production = pd.DataFrame(
        {
            "age": rng.normal(45, 15, N_PRODUCTION).clip(18, 80),
            "income": rng.lognormal(10.5, 0.8, N_PRODUCTION),
            "credit_score": rng.normal(600, 100, N_PRODUCTION).clip(300, 850),
        }
    )
    return DriftScenario(
        name="Data Drift",
        description="Mudança na distribuição das features (age, income, credit_score)",
        reference_data=reference,
        production_data=production,
    )


def simulate_concept_drift(rng: np.random.Generator) -> DriftScenario:
    """Simula concept drift: a relação entre features e target muda.

    Args:
        rng: Gerador de números aleatórios.

    Returns:
        Cenário de concept drift.
    """
    x_ref = rng.normal(0, 1, (N_REFERENCE, 3))
    y_ref = (x_ref[:, 0] + x_ref[:, 1] > 0).astype(int)

    x_prod = rng.normal(0, 1, (N_PRODUCTION, 3))
    y_prod = (x_prod[:, 0] - x_prod[:, 1] > 0).astype(int)

    feature_names = ["feature_1", "feature_2", "feature_3"]
    return DriftScenario(
        name="Concept Drift",
        description="A relação entre features e target mudou (regra de decisão invertida)",
        reference_data=pd.DataFrame(x_ref, columns=feature_names),
        production_data=pd.DataFrame(x_prod, columns=feature_names),
        reference_labels=pd.Series(y_ref),
        production_labels=pd.Series(y_prod),
    )


def simulate_label_drift(rng: np.random.Generator) -> DriftScenario:
    """Simula label drift: mudança na distribuição dos labels.

    Args:
        rng: Gerador de números aleatórios.

    Returns:
        Cenário de label drift.
    """
    x_ref = rng.normal(0, 1, (N_REFERENCE, 4))
    y_ref = rng.choice([0, 1], N_REFERENCE, p=[0.7, 0.3])

    x_prod = rng.normal(0.2, 1, (N_PRODUCTION, 4))
    y_prod = rng.choice([0, 1], N_PRODUCTION, p=[0.4, 0.6])

    feature_names = [f"feature_{i}" for i in range(1, 5)]
    return DriftScenario(
        name="Label Drift",
        description="Proporção de classes mudou: 70/30 → 40/60",
        reference_data=pd.DataFrame(x_ref, columns=feature_names),
        production_data=pd.DataFrame(x_prod, columns=feature_names),
        reference_labels=pd.Series(y_ref),
        production_labels=pd.Series(y_prod),
    )


def build_scenarios(random_state: int = RANDOM_STATE) -> list[DriftScenario]:
    """Constroi os cenarios usados na aula de forma reprodutivel."""
    rng = np.random.default_rng(random_state)
    return [
        simulate_data_drift(rng),
        simulate_concept_drift(rng),
        simulate_label_drift(rng),
    ]


def compute_ks_statistic(reference: np.ndarray, production: np.ndarray) -> float:
    """Calcula a estatistica KS sem depender de SciPy."""
    reference_sorted = np.sort(reference.astype(float))
    production_sorted = np.sort(production.astype(float))
    combined = np.sort(np.concatenate([reference_sorted, production_sorted]))
    reference_cdf = np.searchsorted(reference_sorted, combined, side="right") / len(
        reference_sorted
    )
    production_cdf = np.searchsorted(production_sorted, combined, side="right") / len(
        production_sorted
    )
    return float(np.max(np.abs(reference_cdf - production_cdf)))


def compute_ks_threshold(
    reference_size: int, production_size: int, alpha: float = 0.05
) -> float:
    """Aproxima o limiar critico do teste KS para uso didatico."""
    if alpha != 0.05:
        raise ValueError("Only alpha=0.05 is supported in this lightweight demo")
    coefficient = 1.36
    return float(
        coefficient
        * np.sqrt(
            (reference_size + production_size) / (reference_size * production_size)
        )
    )


def summarize_scenario(scenario: DriftScenario, alpha: float = 0.05) -> DriftSummary:
    """Resume um cenario com KS por feature e delta medio."""
    # No GoF pattern applies; this module is a deterministic data transform for teaching.
    threshold = compute_ks_threshold(
        reference_size=len(scenario.reference_data),
        production_size=len(scenario.production_data),
        alpha=alpha,
    )
    feature_ks: dict[str, float] = {}
    mean_shifts: dict[str, float] = {}
    drifted_features: list[str] = []

    for column in scenario.reference_data.columns:
        reference = scenario.reference_data[column].to_numpy(dtype=float)
        production = scenario.production_data[column].to_numpy(dtype=float)
        statistic = compute_ks_statistic(reference, production)
        feature_ks[column] = statistic
        mean_shifts[column] = float(production.mean() - reference.mean())
        if statistic > threshold:
            drifted_features.append(column)

    label_rate_delta: float | None = None
    if scenario.reference_labels is not None and scenario.production_labels is not None:
        label_rate_delta = float(
            scenario.production_labels.mean() - scenario.reference_labels.mean()
        )

    return DriftSummary(
        name=scenario.name,
        description=scenario.description,
        feature_ks=feature_ks,
        drifted_features=drifted_features,
        mean_shifts=mean_shifts,
        label_rate_delta=label_rate_delta,
    )


def analyze_scenario(scenario: DriftScenario) -> dict[str, float]:
    """Analisa um cenário de drift calculando métricas básicas.

    Args:
        scenario: Cenário de drift a analisar.

    Returns:
        Dicionário com métricas de drift por feature.
    """
    logger.info("\n=== %s ===", scenario.name)
    logger.info("Descrição: %s", scenario.description)
    summary = summarize_scenario(scenario)
    threshold = compute_ks_threshold(
        reference_size=len(scenario.reference_data),
        production_size=len(scenario.production_data),
    )

    drift_scores: dict[str, float] = {}
    for col in scenario.reference_data.columns:
        stat = summary.feature_ks[col]
        drift_scores[col] = float(stat)
        logger.info(
            "KS [%s]: stat=%.4f, threshold=%.4f -> drift=%s",
            col,
            stat,
            threshold,
            "SIM" if col in summary.drifted_features else "NAO",
        )

    if scenario.reference_labels is not None and scenario.production_labels is not None:
        ref_rate = float(scenario.reference_labels.mean())
        prod_rate = float(scenario.production_labels.mean())
        logger.info(
            "Label rate: referência=%.2f, produção=%.2f (Δ=%.2f)",
            ref_rate,
            prod_rate,
            abs(prod_rate - ref_rate),
        )

    return drift_scores


def run_all_scenarios(random_state: int = RANDOM_STATE) -> list[DriftSummary]:
    """Executa todos os cenarios e retorna resumos para smoke tests."""
    scenarios = build_scenarios(random_state=random_state)
    summaries: list[DriftSummary] = []
    for scenario in scenarios:
        analyze_scenario(scenario)
        summaries.append(summarize_scenario(scenario))
    return summaries


if __name__ == "__main__":
    run_all_scenarios()
