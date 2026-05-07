"""Contratos de dados com pandera.

Atende ao requisito ``pytest e pandera`` validando o dataset bruto antes
de qualquer transformação.
"""

from __future__ import annotations

import pandera.pandas as pa
from pandera.pandas import Column, DataFrameSchema

TARGET_COLUMN: str = "MedHouseVal"

RAW_FEATURE_COLUMNS: tuple[str, ...] = (
    "MedInc",
    "HouseAge",
    "AveRooms",
    "AveBedrms",
    "Population",
    "AveOccup",
    "Latitude",
    "Longitude",
)

raw_dataset_schema: DataFrameSchema = DataFrameSchema(
    {
        "MedInc": Column(float, pa.Check.gt(0)),
        "HouseAge": Column(float, pa.Check.ge(0)),
        "AveRooms": Column(float, pa.Check.gt(0)),
        "AveBedrms": Column(float, pa.Check.gt(0)),
        "Population": Column(float, pa.Check.gt(0)),
        "AveOccup": Column(float, pa.Check.gt(0)),
        "Latitude": Column(float, pa.Check.in_range(32.0, 42.5)),
        "Longitude": Column(float, pa.Check.in_range(-125.0, -113.0)),
        TARGET_COLUMN: Column(float, pa.Check.gt(0), nullable=False),
    },
    strict=True,
    coerce=True,
)
