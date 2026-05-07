"""Carregamento, validação e limpeza dos dados (SRP: dados brutos)."""

import pandas as pd
import pandera.pandas as pa
from sklearn.datasets import fetch_california_housing

# Schema do dataset bruto (antes de feature engineering).
raw_schema = pa.DataFrameSchema(
    {
        "MedInc": pa.Column(float, pa.Check.gt(0)),
        "HouseAge": pa.Column(float, pa.Check.ge(0)),
        "AveRooms": pa.Column(float, pa.Check.gt(0)),
        "AveBedrms": pa.Column(float, pa.Check.gt(0)),
        "Population": pa.Column(float, pa.Check.gt(0)),
        "AveOccup": pa.Column(float, pa.Check.gt(0)),
        "Latitude": pa.Column(float, pa.Check.in_range(32, 42)),
        "Longitude": pa.Column(float, pa.Check.in_range(-125, -114)),
        "MedHouseVal": pa.Column(float, pa.Check.gt(0)),
    }
)


def load_data() -> pd.DataFrame:
    """Carrega o California Housing como DataFrame validado."""
    df = fetch_california_housing(as_frame=True).frame
    return raw_schema.validate(df)


def clip_target(df: pd.DataFrame, column: str, upper: float) -> pd.DataFrame:
    """Remove linhas com target acima do limite (não muta o original)."""
    return df[df[column] < upper].reset_index(drop=True)
