"""Anonymization — técnicas de anonimização e privacidade diferencial.

Demonstra técnicas para proteger dados pessoais em modelos de ML:
- Pseudonimização com hash
- Generalização de atributos
- Adição de ruído diferencial

Uso:
    python anonymization.py
"""

import hashlib
import logging

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
DP_EPSILON = 1.0


def pseudonymize_id(value: str, salt: str = "mlet-salt") -> str:
    """Pseudonimiza um identificador com hash SHA-256.

    Substitui identificadores diretos por tokens não revertíveis
    sem a chave de pseudonimização.

    Args:
        value: Valor a pseudonimizar (ex: CPF, email).
        salt: Salt para dificultar ataques por dicionário.

    Returns:
        Hash hexadecimal do identificador.
    """
    combined = f"{salt}:{value}"
    return hashlib.sha256(combined.encode()).hexdigest()[:16]


def generalize_age(age: float, bin_size: int = 10) -> str:
    """Generaliza idade em faixas etárias para k-anonymity.

    Args:
        age: Idade exata.
        bin_size: Tamanho da faixa etária.

    Returns:
        String representando a faixa etária (ex: '30-39').
    """
    lower = int(age // bin_size) * bin_size
    return f"{lower}-{lower + bin_size - 1}"


def add_laplace_noise(
    value: float, sensitivity: float, epsilon: float = DP_EPSILON
) -> float:
    """Adiciona ruído Laplaciano para privacidade diferencial.

    Mecanismo de Laplace: noise ~ Laplace(0, sensitivity/epsilon)

    Args:
        value: Valor original.
        sensitivity: Sensibilidade da função (faixa dos dados).
        epsilon: Parâmetro de privacidade (menor = mais privado).

    Returns:
        Valor com ruído diferencial adicionado.
    """
    scale = sensitivity / epsilon
    rng = np.random.default_rng(RANDOM_STATE)
    noise = rng.laplace(loc=0, scale=scale)
    return float(value + noise)


def anonymize_dataframe(
    df: pd.DataFrame,
    id_columns: list[str],
    age_column: str | None = None,
    numeric_columns_dp: list[str] | None = None,
    epsilon: float = DP_EPSILON,
) -> pd.DataFrame:
    """Anonimiza DataFrame com múltiplas técnicas.

    Args:
        df: DataFrame original com dados sensíveis.
        id_columns: Colunas de identificação a pseudonimizar.
        age_column: Coluna de idade a generalizar (opcional).
        numeric_columns_dp: Colunas numéricas para privacidade diferencial.
        epsilon: Parâmetro epsilon para privacidade diferencial.

    Returns:
        DataFrame anonimizado.
    """
    df_anon = df.copy()

    for col in id_columns:
        if col in df_anon.columns:
            df_anon[col] = df_anon[col].astype(str).apply(pseudonymize_id)
            logger.info("Pseudonimizado: %s", col)

    if age_column and age_column in df_anon.columns:
        df_anon[f"{age_column}_group"] = df_anon[age_column].apply(generalize_age)
        df_anon = df_anon.drop(columns=[age_column])
        logger.info("Generalizado: %s → %s_group", age_column, age_column)

    if numeric_columns_dp:
        for col in numeric_columns_dp:
            if col in df_anon.columns:
                sensitivity = float(df_anon[col].max() - df_anon[col].min())
                df_anon[col] = df_anon[col].apply(
                    lambda v: add_laplace_noise(float(v), sensitivity, epsilon)
                )
                logger.info("DP aplicado a: %s (ε=%.1f)", col, epsilon)

    return df_anon


def demo_anonymization() -> None:
    """Demonstra as técnicas de anonimização."""
    rng = np.random.default_rng(RANDOM_STATE)
    df = pd.DataFrame(
        {
            "cpf": [
                f"{rng.integers(100, 999)}.{rng.integers(100, 999)}.{rng.integers(100, 999)}-{rng.integers(10, 99)}"
                for _ in range(10)
            ],
            "email": [f"user{i}@example.com" for i in range(10)],
            "age": rng.integers(18, 70, 10).astype(float),
            "income": rng.lognormal(10, 0.5, 10),
            "churn": rng.integers(0, 2, 10),
        }
    )

    logger.info("=== Dados Originais ===")
    logger.info(df.to_string(index=False))

    df_anon = anonymize_dataframe(
        df,
        id_columns=["cpf", "email"],
        age_column="age",
        numeric_columns_dp=["income"],
        epsilon=1.0,
    )

    logger.info("\n=== Dados Anonimizados ===")
    logger.info(df_anon.to_string(index=False))
    logger.info("\nColunas removidas: cpf, email, age (substituídas/generalizadas)")


if __name__ == "__main__":
    demo_anonymization()
