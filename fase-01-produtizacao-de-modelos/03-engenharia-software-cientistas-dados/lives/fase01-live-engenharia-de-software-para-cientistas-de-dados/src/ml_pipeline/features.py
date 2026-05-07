"""Engenharia de features.

Responsabilidade única: derivar novas colunas de negócio a partir das
features brutas. Função pura, idempotente sobre as colunas originais.
"""

from __future__ import annotations

import pandas as pd

EPSILON: float = 1e-6

ENGINEERED_COLUMNS: tuple[str, ...] = (
    "rooms_per_household",
    "bedrooms_per_room",
    "population_per_household",
)


def add_engineered_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona features úteis para regressão de preço de imóveis.

    A função é idempotente sobre as colunas de entrada: chamadas
    sucessivas produzem o mesmo resultado.

    Args:
        df: DataFrame com as colunas brutas do California Housing.

    Returns:
        Cópia do DataFrame acrescido de ``ENGINEERED_COLUMNS``.
    """
    out = df.copy()
    out["rooms_per_household"] = out["AveRooms"].astype("float64") / out[
        "HouseAge"
    ].replace(0, 1)
    out["bedrooms_per_room"] = out["AveBedrms"].astype("float64") / (
        out["AveRooms"] + EPSILON
    )
    out["population_per_household"] = out["Population"].astype("float64") / (
        out["AveOccup"] + EPSILON
    )
    return out
