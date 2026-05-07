import pandas as pd

from ml_pipeline.preprocessing import clip_target_outliers


def test_clip_remove_linhas_acima_do_limite() -> None:
    df = pd.DataFrame({"y": [1.0, 4.9, 5.0, 5.5]})
    out = clip_target_outliers(df, target_column="y", upper=5.0)
    assert out["y"].tolist() == [1.0, 4.9]


def test_clip_preserva_indice_zero_based() -> None:
    df = pd.DataFrame({"y": [1.0, 6.0, 2.0]})
    out = clip_target_outliers(df, target_column="y", upper=5.0)
    assert list(out.index) == [0, 1]


def test_clip_nao_modifica_dataframe_original() -> None:
    df = pd.DataFrame({"y": [1.0, 6.0]})
    snapshot = df.copy()
    clip_target_outliers(df, target_column="y", upper=5.0)
    pd.testing.assert_frame_equal(df, snapshot)
