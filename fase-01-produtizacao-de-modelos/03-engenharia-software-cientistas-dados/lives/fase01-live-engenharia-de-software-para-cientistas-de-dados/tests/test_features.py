import numpy as np
import pandas as pd
import pytest

from ml_pipeline.features import ENGINEERED_COLUMNS, add_engineered_features


@pytest.fixture
def sample_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "MedInc": [3.0, 4.5, 2.1],
            "HouseAge": [10.0, 0.0, 25.0],
            "AveRooms": [5.0, 6.0, 4.0],
            "AveBedrms": [1.0, 1.5, 0.8],
            "Population": [1000.0, 800.0, 1500.0],
            "AveOccup": [3.0, 2.5, 4.0],
            "Latitude": [34.0, 35.0, 36.0],
            "Longitude": [-118.0, -119.0, -120.0],
        }
    )


def test_features_geram_colunas_esperadas(sample_frame: pd.DataFrame) -> None:
    out = add_engineered_features(sample_frame)
    for column in ENGINEERED_COLUMNS:
        assert column in out.columns


def test_features_preservam_numero_de_linhas(sample_frame: pd.DataFrame) -> None:
    assert len(add_engineered_features(sample_frame)) == len(sample_frame)


def test_features_sao_idempotentes_sobre_colunas_originais(
    sample_frame: pd.DataFrame,
) -> None:
    once = add_engineered_features(sample_frame)
    twice = add_engineered_features(once)
    pd.testing.assert_frame_equal(once, twice[once.columns])


def test_features_nao_introduzem_nan_nem_inf(sample_frame: pd.DataFrame) -> None:
    out = add_engineered_features(sample_frame)
    valores = out[list(ENGINEERED_COLUMNS)].to_numpy()
    assert not np.isnan(valores).any()
    assert not np.isinf(valores).any()


def test_features_engineered_sao_float64(sample_frame: pd.DataFrame) -> None:
    out = add_engineered_features(sample_frame)
    for column in ENGINEERED_COLUMNS:
        assert out[column].dtype == np.float64
