from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from ml_pipeline.models import MODEL_REGISTRY


def test_registry_contem_cinco_modelos() -> None:
    assert len(MODEL_REGISTRY) == 5


def test_factories_retornam_pipeline_com_scaler_e_estimator() -> None:
    for name, factory in MODEL_REGISTRY.items():
        pipe = factory(random_state=0)
        assert isinstance(pipe, Pipeline), name
        assert isinstance(pipe.named_steps["scaler"], StandardScaler), name
        assert pipe.named_steps["estimator"] is not None, name


def test_modelos_sao_reproducíveis_com_mesma_semente() -> None:
    factory = MODEL_REGISTRY["random_forest"]
    a = factory(random_state=7)
    b = factory(random_state=7)
    assert (
        a.named_steps["estimator"].random_state
        == b.named_steps["estimator"].random_state
    )
