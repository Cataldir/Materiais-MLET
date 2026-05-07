"""Pré-processamento de dados.

Responsabilidade única: limpar o dataset bruto. Não faz feature
engineering nem split.
"""

from __future__ import annotations

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clip_target_outliers(
    df: pd.DataFrame, target_column: str, upper: float
) -> pd.DataFrame:
    """Remove linhas onde o target está saturado no limite superior.

    Args:
        df: DataFrame de entrada.
        target_column: Nome da coluna alvo.
        upper: Valor limite (estritamente menor para manter a linha).

    Returns:
        Cópia do DataFrame sem as linhas saturadas, com índice resetado.
    """
    mask = df[target_column] < upper
    removed = int((~mask).sum())
    if removed:
        logger.info("Removidas %d linhas com %s >= %.2f", removed, target_column, upper)
    return df.loc[mask].reset_index(drop=True)
