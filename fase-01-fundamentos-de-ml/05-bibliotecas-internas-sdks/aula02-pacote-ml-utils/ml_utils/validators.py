"""Validadores de dados para pipelines de ML.

Fornece funções para validação de DataFrames antes do treinamento,
detectando problemas comuns que podem afetar a qualidade dos modelos.

Exemplo:
    >>> from ml_utils.validators import validate_dataframe
    >>> issues = validate_dataframe(df, required_columns=["age", "survived"])
    >>> if issues:
    ...     raise ValueError(f"Problemas encontrados: {issues}")
"""

import logging
from typing import Any

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def validate_dataframe(
    df: pd.DataFrame,
    required_columns: list[str] | None = None,
    max_missing_ratio: float = 0.5,
    min_rows: int = 10,
) -> list[str]:
    """Valida um DataFrame para uso em pipeline de ML.

    Args:
        df: DataFrame a validar.
        required_columns: Colunas obrigatórias.
        max_missing_ratio: Proporção máxima de valores faltantes por coluna.
        min_rows: Número mínimo de linhas.

    Returns:
        Lista de problemas encontrados (vazia se tudo OK).
    """
    issues: list[str] = []

    if len(df) < min_rows:
        issues.append(f"DataFrame tem apenas {len(df)} linhas (mínimo: {min_rows})")

    if required_columns:
        missing_cols = [c for c in required_columns if c not in df.columns]
        if missing_cols:
            issues.append(f"Colunas obrigatórias faltando: {missing_cols}")

    for col in df.columns:
        missing_ratio = df[col].isna().mean()
        if missing_ratio > max_missing_ratio:
            issues.append(
                f"Coluna '{col}' tem {missing_ratio:.1%} de valores faltantes "
                f"(máximo: {max_missing_ratio:.1%})"
            )

    if issues:
        for issue in issues:
            logger.warning("Validação: %s", issue)
    else:
        logger.info("Validação OK: %d linhas, %d colunas", len(df), len(df.columns))

    return issues


def check_feature_types(
    df: pd.DataFrame,
    expected_types: dict[str, type],
) -> list[str]:
    """Verifica tipos de features esperados.

    Args:
        df: DataFrame a verificar.
        expected_types: Mapeamento coluna → tipo Python esperado.

    Returns:
        Lista de incompatibilidades de tipo.
    """
    issues: list[str] = []
    for col, expected_type in expected_types.items():
        if col not in df.columns:
            issues.append(f"Coluna '{col}' não encontrada")
            continue
        actual_dtype = df[col].dtype
        is_numeric = np.issubdtype(actual_dtype, np.number)
        if expected_type in (int, float) and not is_numeric:
            issues.append(
                f"Coluna '{col}' deveria ser numérica, mas é {actual_dtype}"
            )
    return issues
