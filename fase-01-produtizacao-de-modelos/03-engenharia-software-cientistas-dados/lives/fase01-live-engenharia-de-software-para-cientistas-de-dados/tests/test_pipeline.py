"""Teste de integração do pipeline."""

from ml_pipeline.config import PipelineConfig
from ml_pipeline.pipeline import run


def test_run_gera_artefatos_e_modelo_razoavel(tmp_path):
    config = PipelineConfig(artifacts_dir=tmp_path, random_state=42)
    best = run(config)

    assert best["r2"] > 0.5
    assert (tmp_path / "best_model.pkl").exists()
    assert (tmp_path / "metrics.json").exists()
