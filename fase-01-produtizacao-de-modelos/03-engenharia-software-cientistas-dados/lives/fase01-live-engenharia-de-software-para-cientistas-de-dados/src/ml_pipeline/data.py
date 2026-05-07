"""Carregamento de dados.

Responsabilidade única: obter o DataFrame bruto e validar contrato.
"""

from __future__ import annotations

import logging

import pandas as pd
from sklearn.datasets import fetch_california_housing

from ml_pipeline.schemas import raw_dataset_schema

logger = logging.getLogger(__name__)


def load_california_housing() -> pd.DataFrame:
    """Carrega o dataset California Housing como DataFrame validado.

    Returns:
        DataFrame que satisfaz ``raw_dataset_schema``.
    """
    bundle = fetch_california_housing(as_frame=True)
    df = bundle.frame
    logger.info("Dataset carregado: %d linhas, %d colunas", *df.shape)
    return raw_dataset_schema.validate(df)
