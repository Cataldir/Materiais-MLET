"""Drift detection — detecção manual de data drift em produção.

Implementa testes estatísticos básicos para detectar mudanças na
distribuição de dados entre referência e produção.

Uso:
    python drift_detection.py
"""

import logging

import numpy as np
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ALPHA = 0.05
RANDOM_STATE = 42


def kolmogorov_smirnov_test(
    reference: np.ndarray, production: np.ndarray, feature_name: str
) -> dict[str, float]:
    """Aplica teste Kolmogorov-Smirnov para detectar drift.

    Args:
        reference: Distribuição de referência (treino).
        production: Distribuição de produção (inferência recente).
        feature_name: Nome da feature para logging.

    Returns:
        Dicionário com estatística KS e p-value.
    """
    statistic, p_value = stats.ks_2samp(reference, production)
    has_drift = p_value < ALPHA
    logger.info(
        "KS Test [%s]: stat=%.4f, p=%.4f → drift=%s",
        feature_name, statistic, p_value, "⚠️  SIM" if has_drift else "✓ NÃO",
    )
    return {"statistic": float(statistic), "p_value": float(p_value), "drift": has_drift}


def population_stability_index(
    reference: np.ndarray,
    production: np.ndarray,
    n_bins: int = 10,
) -> float:
    """Calcula o Population Stability Index (PSI).

    PSI < 0.1: Sem mudança significativa
    PSI 0.1-0.2: Mudança moderada — monitorar
    PSI > 0.2: Mudança significativa — investigar

    Args:
        reference: Distribuição de referência.
        production: Distribuição de produção.
        n_bins: Número de bins para discretização.

    Returns:
        Valor do PSI.
    """
    bins = np.percentile(reference, np.linspace(0, 100, n_bins + 1))
    bins[0] = -np.inf
    bins[-1] = np.inf

    ref_pct = np.histogram(reference, bins=bins)[0] / len(reference)
    prod_pct = np.histogram(production, bins=bins)[0] / len(production)

    ref_pct = np.where(ref_pct == 0, 1e-6, ref_pct)
    prod_pct = np.where(prod_pct == 0, 1e-6, prod_pct)

    psi = np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct))

    level = "SEM DRIFT" if psi < 0.1 else "MODERADO" if psi < 0.2 else "CRÍTICO"
    logger.info("PSI: %.4f → %s", psi, level)
    return float(psi)


def simulate_drift_scenario(scenario: str, rng: np.random.Generator) -> tuple[np.ndarray, np.ndarray]:
    """Simula diferentes cenários de drift para demonstração.

    Args:
        scenario: Tipo de cenário ('none', 'shift', 'scale', 'skew').
        rng: Gerador de números aleatórios.

    Returns:
        Tupla (referência, produção).
    """
    reference = rng.normal(loc=0, scale=1, size=1000)

    scenarios = {
        "none": lambda: rng.normal(loc=0, scale=1, size=500),
        "shift": lambda: rng.normal(loc=1.5, scale=1, size=500),
        "scale": lambda: rng.normal(loc=0, scale=2.5, size=500),
        "skew": lambda: rng.exponential(scale=1, size=500),
    }
    production = scenarios.get(scenario, scenarios["none"])()
    return reference, production


def run_drift_analysis() -> None:
    """Executa análise de drift em múltiplos cenários simulados."""
    rng = np.random.default_rng(RANDOM_STATE)

    for scenario in ["none", "shift", "scale", "skew"]:
        logger.info("\n=== Cenário: %s ===", scenario.upper())
        reference, production = simulate_drift_scenario(scenario, rng)
        kolmogorov_smirnov_test(reference, production, "feature_simulada")
        population_stability_index(reference, production)


if __name__ == "__main__":
    run_drift_analysis()
