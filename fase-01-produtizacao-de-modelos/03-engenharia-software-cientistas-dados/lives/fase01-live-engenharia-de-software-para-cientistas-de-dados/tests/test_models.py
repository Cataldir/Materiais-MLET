"""Testes do módulo models."""

from sklearn.pipeline import Pipeline

from ml_pipeline.models import build_models, evaluate


def test_registry_tem_cinco_modelos():
    models = build_models(random_state=42)
    assert len(models) == 4


def test_modelos_sao_pipelines_com_scaler():
    for model in build_models(random_state=42).values():
        assert isinstance(model, Pipeline)
        assert "scaler" in model.named_steps


def test_evaluate_retorna_metricas_basicas():
    metrics = evaluate([1.0, 2.0, 3.0], [1.0, 2.0, 3.0])
    assert metrics["rmse"] == 0.0
    assert metrics["mae"] == 0.0
    assert metrics["r2"] == 1.0
