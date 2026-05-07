"""Engenharia de features (SRP: criar colunas derivadas)."""

import pandas as pd

EPS = 1e-6


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Adiciona features derivadas. Não muta o DataFrame original."""
    out = df.copy()
    out["rooms_per_household"] = out["AveRooms"] / (out["HouseAge"] + EPS)
    out["bedrooms_per_room"] = out["AveBedrms"] / (out["AveRooms"] + EPS)
    out["population_per_household"] = out["Population"] / (out["AveOccup"] + EPS)
    return out
