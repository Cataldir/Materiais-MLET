"""Statistical Tests — implementação de testes para detecção de drift.

Implementa KS test, PSI, Chi-squared e Jensen-Shannon Divergence
para detectar mudanças na distribuição de dados.

Uso:
    python statistical_tests.py
"""

import logging

import numpy as np
import pandas as pd
from scipy import stats
from scipy.spatial.distance import jensenshannon

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

ALPHA = 0.05
RANDOM_STATE = 42


def ks_test(
    reference: np.ndarray,
    production: np.ndarray,
    feature_name: str = "feature",
) -> dict[str, float | bool]:
    """Teste Kolmogorov-Smirnov para detecção de drift em variáveis contínuas.

    Args:
        reference: Distribuição de referência.
        production: Distribuição de produção.
        feature_name: Nome da feature para logging.

    Returns:
        Dicionário com estatística, p-value e flag de drift.
    """
    statistic, p_value = stats.ks_2samp(reference, production)
    has_drift = bool(p_value < ALPHA)
    logger.info(
        "KS [%s]: stat=%.4f, p=%.4f → drift=%s",
        feature_name, statistic, p_value, "SIM" if has_drift else "NÃO"
    )
    return {
        "test": "ks",
        "feature": feature_name,
        "statistic": float(statistic),
        "p_value": float(p_value),
        "drift_detected": has_drift,
    }


def psi_test(
    reference: np.ndarray,
    production: np.ndarray,
    n_bins: int = 10,
    feature_name: str = "feature",
) -> dict[str, float | bool]:
    """Population Stability Index (PSI) para detecção de drift.

    Interpretação: PSI < 0.1 = estável, 0.1-0.2 = moderado, > 0.2 = crítico

    Args:
        reference: Distribuição de referência.
        production: Distribuição de produção.
        n_bins: Número de bins para discretização.
        feature_name: Nome da feature.

    Returns:
        Dicionário com PSI e flag de drift.
    """
    bins = np.percentile(reference, np.linspace(0, 100, n_bins + 1))
    bins[0] = -np.inf
    bins[-1] = np.inf

    ref_counts = np.histogram(reference, bins=bins)[0]
    prod_counts = np.histogram(production, bins=bins)[0]

    ref_pct = ref_counts / len(reference)
    prod_pct = prod_counts / len(production)

    ref_pct = np.where(ref_pct == 0, 1e-6, ref_pct)
    prod_pct = np.where(prod_pct == 0, 1e-6, prod_pct)

    psi_value = float(np.sum((prod_pct - ref_pct) * np.log(prod_pct / ref_pct)))
    level = "ESTÁVEL" if psi_value < 0.1 else "MODERADO" if psi_value < 0.2 else "CRÍTICO"
    has_drift = psi_value >= 0.1

    logger.info("PSI [%s]: %.4f → %s", feature_name, psi_value, level)
    return {
        "test": "psi",
        "feature": feature_name,
        "psi": psi_value,
        "level": level,
        "drift_detected": has_drift,
    }


def chi2_test(
    reference_counts: np.ndarray,
    production_counts: np.ndarray,
    feature_name: str = "feature",
) -> dict[str, float | bool]:
    """Teste Chi-quadrado para drift em variáveis categóricas.

    Args:
        reference_counts: Contagens por categoria na referência.
        production_counts: Contagens por categoria na produção.
        feature_name: Nome da feature.

    Returns:
        Dicionário com estatística Chi2, p-value e flag de drift.
    """
    n_ref = reference_counts.sum()
    n_prod = production_counts.sum()
    expected = reference_counts * (n_prod / n_ref)
    statistic, p_value = stats.chisquare(production_counts, f_exp=expected)
    has_drift = bool(p_value < ALPHA)
    logger.info(
        "Chi2 [%s]: stat=%.4f, p=%.4f → drift=%s",
        feature_name, statistic, p_value, "SIM" if has_drift else "NÃO"
    )
    return {
        "test": "chi2",
        "feature": feature_name,
        "statistic": float(statistic),
        "p_value": float(p_value),
        "drift_detected": has_drift,
    }


def js_divergence(
    reference: np.ndarray,
    production: np.ndarray,
    n_bins: int = 20,
    feature_name: str = "feature",
) -> dict[str, float | bool]:
    """Jensen-Shannon Divergence para comparação de distribuições.

    JS divergence é simétrica e limitada a [0, 1] (na versão sqrt).

    Args:
        reference: Distribuição de referência.
        production: Distribuição de produção.
        n_bins: Bins para histograma.
        feature_name: Nome da feature.

    Returns:
        Dicionário com JSD e flag de drift.
    """
    all_values = np.concatenate([reference, production])
    bins = np.linspace(all_values.min(), all_values.max(), n_bins + 1)

    ref_hist = np.histogram(reference, bins=bins, density=True)[0]
    prod_hist = np.histogram(production, bins=bins, density=True)[0]

    ref_hist = ref_hist / (ref_hist.sum() + 1e-10)
    prod_hist = prod_hist / (prod_hist.sum() + 1e-10)

    jsd = float(jensenshannon(ref_hist, prod_hist))
    has_drift = jsd > 0.1

    logger.info("JSD [%s]: %.4f → drift=%s", feature_name, jsd, "SIM" if has_drift else "NÃO")
    return {
        "test": "jsd",
        "feature": feature_name,
        "jsd": jsd,
        "drift_detected": has_drift,
    }


def run_comprehensive_drift_analysis() -> pd.DataFrame:
    """Executa análise completa de drift com todos os testes.

    Returns:
        DataFrame com resultados de todos os testes.
    """
    rng = np.random.default_rng(RANDOM_STATE)
    reference = rng.normal(0, 1, 1000)
    production_drift = rng.normal(1.5, 1.5, 500)
    production_stable = rng.normal(0, 1, 500)

    logger.info("=== Dados COM drift ===")
    results = []
    results.append(ks_test(reference, production_drift, "feature_drifted"))
    results.append(psi_test(reference, production_drift, feature_name="feature_drifted"))
    results.append(js_divergence(reference, production_drift, feature_name="feature_drifted"))

    logger.info("\n=== Dados SEM drift ===")
    results.append(ks_test(reference, production_stable, "feature_stable"))
    results.append(psi_test(reference, production_stable, feature_name="feature_stable"))
    results.append(js_divergence(reference, production_stable, feature_name="feature_stable"))

    logger.info("\n=== Drift Categórico (Chi2) ===")
    ref_counts = np.array([300, 400, 300])
    prod_counts = np.array([150, 200, 150])
    results.append(chi2_test(ref_counts, prod_counts, "category"))

    return pd.DataFrame(results)


if __name__ == "__main__":
    df_results = run_comprehensive_drift_analysis()
    logger.info("\n=== Resumo ===\n%s", df_results.to_string(index=False))
