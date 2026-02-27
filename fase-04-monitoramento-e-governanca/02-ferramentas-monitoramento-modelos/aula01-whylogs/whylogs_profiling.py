"""whylogs Profiling — monitoramento de qualidade de dados em produção.

Demonstra como usar whylogs para criar perfis de dados e detectar
anomalias e drift automaticamente.

Requisitos:
    pip install whylogs

Uso:
    python whylogs_profiling.py
"""

import logging
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
PROFILES_DIR = Path("profiles")


def generate_reference_data(rng: np.random.Generator) -> pd.DataFrame:
    """Gera dataset de referência (simulando dados de treino).

    Args:
        rng: Gerador de números aleatórios.

    Returns:
        DataFrame de referência.
    """
    return pd.DataFrame({
        "age": rng.normal(35, 10, 1000).clip(18, 80),
        "income": rng.lognormal(10, 0.5, 1000),
        "credit_score": rng.normal(650, 80, 1000).clip(300, 850),
        "prediction": rng.choice([0, 1], 1000, p=[0.7, 0.3]),
    })


def generate_production_batch(
    rng: np.random.Generator, with_drift: bool = False
) -> pd.DataFrame:
    """Gera um batch de dados de produção.

    Args:
        rng: Gerador de números aleatórios.
        with_drift: Se True, injeta drift nos dados.

    Returns:
        DataFrame de produção.
    """
    if with_drift:
        return pd.DataFrame({
            "age": rng.normal(50, 15, 200).clip(18, 80),
            "income": rng.lognormal(11, 0.8, 200),
            "credit_score": rng.normal(580, 120, 200).clip(300, 850),
            "prediction": rng.choice([0, 1], 200, p=[0.45, 0.55]),
        })
    return pd.DataFrame({
        "age": rng.normal(36, 10, 200).clip(18, 80),
        "income": rng.lognormal(10.1, 0.5, 200),
        "credit_score": rng.normal(648, 82, 200).clip(300, 850),
        "prediction": rng.choice([0, 1], 200, p=[0.69, 0.31]),
    })


def profile_with_whylogs(df: pd.DataFrame, dataset_name: str) -> None:
    """Cria perfil de dados com whylogs.

    Args:
        df: DataFrame a ser perfilado.
        dataset_name: Nome do dataset para o perfil.
    """
    try:
        import whylogs as why

        PROFILES_DIR.mkdir(exist_ok=True)
        results = why.log(df)
        profile = results.profile()
        profile_view = profile.view()

        profile_path = PROFILES_DIR / f"{dataset_name}_profile.bin"
        profile.write(profile_path.as_posix())

        logger.info("Perfil '%s' salvo em: %s", dataset_name, profile_path)

        summary = profile_view.to_pandas()
        logger.info("Resumo do perfil (%d features):", len(summary))
        for col in df.columns:
            stats_row = summary[summary.index.get_level_values(0) == col]
            if not stats_row.empty:
                logger.info("  %s: %d não-nulos", col, df[col].notna().sum())

    except ImportError:
        logger.warning("whylogs não instalado. pip install whylogs")
        logger.info("Estatísticas básicas de '%s':", dataset_name)
        logger.info(df.describe().to_string())


def demo_whylogs_monitoring() -> None:
    """Demonstra monitoramento com whylogs em dados de referência e produção."""
    rng = np.random.default_rng(RANDOM_STATE)

    logger.info("=== Criando perfil de referência ===")
    ref_data = generate_reference_data(rng)
    profile_with_whylogs(ref_data, "reference")

    logger.info("\n=== Criando perfil de produção (sem drift) ===")
    prod_stable = generate_production_batch(rng, with_drift=False)
    profile_with_whylogs(prod_stable, "production_stable")

    logger.info("\n=== Criando perfil de produção (com drift) ===")
    prod_drift = generate_production_batch(rng, with_drift=True)
    profile_with_whylogs(prod_drift, "production_drift")

    logger.info("\n=== Comparação manual de médias ===")
    for col in ["age", "income", "credit_score"]:
        ref_mean = ref_data[col].mean()
        prod_mean = prod_drift[col].mean()
        change_pct = abs(prod_mean - ref_mean) / ref_mean * 100
        logger.info(
            "%s: ref=%.2f, prod=%.2f (Δ=%.1f%%)",
            col, ref_mean, prod_mean, change_pct
        )


if __name__ == "__main__":
    demo_whylogs_monitoring()
