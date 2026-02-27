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


def simulate_data_drift(rng: np.random.Generator) -> DriftScenario:
    """Simula data drift: mudança na distribuição das features de entrada.

    Args:
        rng: Gerador de números aleatórios.

    Returns:
        Cenário de data drift.
    """
    reference = pd.DataFrame({
        "age": rng.normal(35, 10, N_REFERENCE).clip(18, 80),
        "income": rng.lognormal(10, 0.5, N_REFERENCE),
        "credit_score": rng.normal(650, 80, N_REFERENCE).clip(300, 850),
    })
    production = pd.DataFrame({
        "age": rng.normal(45, 15, N_PRODUCTION).clip(18, 80),
        "income": rng.lognormal(10.5, 0.8, N_PRODUCTION),
        "credit_score": rng.normal(600, 100, N_PRODUCTION).clip(300, 850),
    })
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
    X_ref = rng.normal(0, 1, (N_REFERENCE, 3))
    y_ref = (X_ref[:, 0] + X_ref[:, 1] > 0).astype(int)

    X_prod = rng.normal(0, 1, (N_PRODUCTION, 3))
    y_prod = (X_prod[:, 0] - X_prod[:, 1] > 0).astype(int)

    feature_names = ["feature_1", "feature_2", "feature_3"]
    return DriftScenario(
        name="Concept Drift",
        description="A relação entre features e target mudou (regra de decisão invertida)",
        reference_data=pd.DataFrame(X_ref, columns=feature_names),
        production_data=pd.DataFrame(X_prod, columns=feature_names),
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
    X_ref = rng.normal(0, 1, (N_REFERENCE, 4))
    y_ref = rng.choice([0, 1], N_REFERENCE, p=[0.7, 0.3])

    X_prod = rng.normal(0.2, 1, (N_PRODUCTION, 4))
    y_prod = rng.choice([0, 1], N_PRODUCTION, p=[0.4, 0.6])

    feature_names = [f"feature_{i}" for i in range(1, 5)]
    return DriftScenario(
        name="Label Drift",
        description="Proporção de classes mudou: 70/30 → 40/60",
        reference_data=pd.DataFrame(X_ref, columns=feature_names),
        production_data=pd.DataFrame(X_prod, columns=feature_names),
        reference_labels=pd.Series(y_ref),
        production_labels=pd.Series(y_prod),
    )


def analyze_scenario(scenario: DriftScenario) -> dict[str, float]:
    """Analisa um cenário de drift calculando métricas básicas.

    Args:
        scenario: Cenário de drift a analisar.

    Returns:
        Dicionário com métricas de drift por feature.
    """
    from scipy import stats

    logger.info("\n=== %s ===", scenario.name)
    logger.info("Descrição: %s", scenario.description)

    drift_scores: dict[str, float] = {}
    for col in scenario.reference_data.columns:
        ref = scenario.reference_data[col].values
        prod = scenario.production_data[col].values
        stat, p_value = stats.ks_2samp(ref, prod)
        drift_scores[col] = float(stat)
        logger.info(
            "KS [%s]: stat=%.4f, p=%.4f → drift=%s",
            col, stat, p_value, "⚠️  SIM" if p_value < 0.05 else "✓ NÃO"
        )

    if scenario.reference_labels is not None and scenario.production_labels is not None:
        ref_rate = float(scenario.reference_labels.mean())
        prod_rate = float(scenario.production_labels.mean())
        logger.info(
            "Label rate: referência=%.2f, produção=%.2f (Δ=%.2f)",
            ref_rate, prod_rate, abs(prod_rate - ref_rate)
        )

    return drift_scores


def run_all_scenarios() -> None:
    """Executa todos os cenários de drift simulados."""
    rng = np.random.default_rng(RANDOM_STATE)
    scenarios = [
        simulate_data_drift(rng),
        simulate_concept_drift(rng),
        simulate_label_drift(rng),
    ]
    for scenario in scenarios:
        analyze_scenario(scenario)


if __name__ == "__main__":
    run_all_scenarios()
