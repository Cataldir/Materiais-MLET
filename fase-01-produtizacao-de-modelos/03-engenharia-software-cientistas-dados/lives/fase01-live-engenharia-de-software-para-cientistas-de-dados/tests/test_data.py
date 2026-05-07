"""Testes do módulo data."""

import pandas as pd
import pytest
from pandera.errors import SchemaError

from ml_pipeline.data import clip_target, raw_schema


def test_schema_aceita_dataset_real(raw_df):
    raw_schema.validate(raw_df)


def test_schema_rejeita_target_negativo(raw_df):
    bad = raw_df.copy()
    bad.loc[0, "MedHouseVal"] = -1.0
    with pytest.raises(SchemaError):
        raw_schema.validate(bad)


def test_clip_target_remove_acima_do_limite():
    df = pd.DataFrame({"y": [1.0, 4.9, 5.0, 5.5]})
    out = clip_target(df, "y", upper=5.0)
    assert out["y"].tolist() == [1.0, 4.9]
