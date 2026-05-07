import pandas as pd
import pytest
from pandera.errors import SchemaError

from ml_pipeline.schemas import RAW_FEATURE_COLUMNS, TARGET_COLUMN, raw_dataset_schema


def test_schema_aceita_dataset_real(raw_dataset: pd.DataFrame) -> None:
    raw_dataset_schema.validate(raw_dataset)


def test_schema_rejeita_target_negativo(raw_dataset: pd.DataFrame) -> None:
    bad = raw_dataset.copy()
    bad.loc[0, TARGET_COLUMN] = -1.0
    with pytest.raises(SchemaError):
        raw_dataset_schema.validate(bad)


def test_schema_rejeita_latitude_fora_de_range(raw_dataset: pd.DataFrame) -> None:
    bad = raw_dataset.copy()
    bad.loc[0, "Latitude"] = 10.0
    with pytest.raises(SchemaError):
        raw_dataset_schema.validate(bad)


def test_schema_lista_features_brutas_esperadas(raw_dataset: pd.DataFrame) -> None:
    for column in RAW_FEATURE_COLUMNS:
        assert column in raw_dataset.columns
