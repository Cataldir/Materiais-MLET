"""Testes do módulo features."""

import pandas as pd

from ml_pipeline.features import add_features


def test_add_features_cria_colunas_esperadas():
    df = pd.DataFrame(
        {
            "AveRooms": [5.0],
            "HouseAge": [10.0],
            "AveBedrms": [1.0],
            "Population": [100.0],
            "AveOccup": [2.0],
        }
    )
    out = add_features(df)
    for col in ("rooms_per_household", "bedrooms_per_room", "population_per_household"):
        assert col in out.columns


def test_add_features_nao_muta_original():
    df = pd.DataFrame(
        {
            "AveRooms": [5.0],
            "HouseAge": [10.0],
            "AveBedrms": [1.0],
            "Population": [100.0],
            "AveOccup": [2.0],
        }
    )
    snapshot = df.copy()
    add_features(df)
    pd.testing.assert_frame_equal(df, snapshot)
