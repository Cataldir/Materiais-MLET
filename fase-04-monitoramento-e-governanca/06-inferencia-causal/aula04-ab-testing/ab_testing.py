"""A/B Testing — análise estatística com abordagem causal.

Demonstra como analisar experimentos A/B com rigor estatístico,
incluindo testes de hipótese, power analysis e intervalos de confiança.

Uso:
    python ab_testing.py
"""

import logging

import numpy as np
import pandas as pd
from scipy import stats

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
ALPHA = 0.05


def simulate_ab_experiment(
    n_control: int = 1000,
    n_treatment: int = 1000,
    control_conversion_rate: float = 0.10,
    treatment_effect: float = 0.02,
    rng: np.random.Generator | None = None,
) -> pd.DataFrame:
    """Simula um experimento A/B de conversão.

    Args:
        n_control: Tamanho do grupo controle.
        n_treatment: Tamanho do grupo tratamento.
        control_conversion_rate: Taxa de conversão do controle.
        treatment_effect: Efeito adicional do tratamento (lift).
        rng: Gerador de números aleatórios.

    Returns:
        DataFrame com resultados do experimento.
    """
    if rng is None:
        rng = np.random.default_rng(RANDOM_STATE)

    treatment_rate = control_conversion_rate + treatment_effect
    control = pd.DataFrame({
        "group": "control",
        "converted": rng.binomial(1, control_conversion_rate, n_control),
    })
    treatment = pd.DataFrame({
        "group": "treatment",
        "converted": rng.binomial(1, treatment_rate, n_treatment),
    })
    return pd.concat([control, treatment], ignore_index=True)


def analyze_ab_test(df: pd.DataFrame, metric_col: str = "converted") -> dict[str, float]:
    """Analisa os resultados de um experimento A/B.

    Realiza teste t de Student (ou teste z para proporções) e calcula
    o tamanho do efeito (Cohen's h para proporções).

    Args:
        df: DataFrame com colunas 'group' e a coluna de métrica.
        metric_col: Nome da coluna de métrica binária.

    Returns:
        Dicionário com estatísticas do experimento.
    """
    control = df[df["group"] == "control"][metric_col].values
    treatment = df[df["group"] == "treatment"][metric_col].values

    control_rate = float(control.mean())
    treatment_rate = float(treatment.mean())
    lift = (treatment_rate - control_rate) / (control_rate + 1e-8)

    statistic, p_value = stats.ttest_ind(control, treatment)

    cohen_h = float(
        2 * np.arcsin(np.sqrt(treatment_rate)) -
        2 * np.arcsin(np.sqrt(control_rate))
    )

    ci_control = stats.norm.interval(
        1 - ALPHA, loc=control_rate,
        scale=np.sqrt(control_rate * (1 - control_rate) / len(control))
    )
    ci_treatment = stats.norm.interval(
        1 - ALPHA, loc=treatment_rate,
        scale=np.sqrt(treatment_rate * (1 - treatment_rate) / len(treatment))
    )

    result = {
        "control_rate": control_rate,
        "treatment_rate": treatment_rate,
        "lift": lift,
        "absolute_lift": treatment_rate - control_rate,
        "t_statistic": float(statistic),
        "p_value": float(p_value),
        "significant": bool(p_value < ALPHA),
        "cohen_h": cohen_h,
    }

    logger.info("=== Resultados do Experimento A/B ===")
    logger.info("Controle: n=%d, taxa=%.3f (IC: [%.3f, %.3f])",
                len(control), control_rate, *ci_control)
    logger.info("Tratamento: n=%d, taxa=%.3f (IC: [%.3f, %.3f])",
                len(treatment), treatment_rate, *ci_treatment)
    logger.info("Lift: %+.1f%% | p-value: %.4f | Significante: %s",
                lift * 100, p_value, "✓ SIM" if result["significant"] else "✗ NÃO")
    logger.info("Cohen's h: %.4f (efeito %s)",
                cohen_h, "pequeno" if abs(cohen_h) < 0.2 else "médio" if abs(cohen_h) < 0.5 else "grande")
    return result


def power_analysis(
    effect_size: float = 0.02,
    baseline_rate: float = 0.10,
    power: float = 0.80,
) -> int:
    """Calcula o tamanho de amostra necessário para o experimento.

    Args:
        effect_size: Efeito mínimo detectável (absoluto).
        baseline_rate: Taxa de conversão da linha de base.
        power: Poder estatístico desejado (1 - beta).

    Returns:
        Tamanho de amostra mínimo por grupo.
    """
    p1 = baseline_rate
    p2 = baseline_rate + effect_size
    h = abs(2 * np.arcsin(np.sqrt(p2)) - 2 * np.arcsin(np.sqrt(p1)))

    z_alpha = stats.norm.ppf(1 - ALPHA / 2)
    z_beta = stats.norm.ppf(power)
    n = int(np.ceil(((z_alpha + z_beta) / h) ** 2))

    logger.info(
        "Power Analysis: efeito=%.1f%%, baseline=%.1f%%, power=%.0f%% → n=%d por grupo",
        effect_size * 100, baseline_rate * 100, power * 100, n
    )
    return n


if __name__ == "__main__":
    logger.info("=== Power Analysis ===")
    required_n = power_analysis(effect_size=0.02, baseline_rate=0.10)

    logger.info("\n=== Simulação de Experimento ===")
    rng = np.random.default_rng(RANDOM_STATE)
    df_experiment = simulate_ab_experiment(n_control=required_n, n_treatment=required_n, rng=rng)
    analyze_ab_test(df_experiment)
