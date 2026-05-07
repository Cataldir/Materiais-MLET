"""Smoke test do orquestrador.

Inclui um teste com fake persister para provar DIP: o pipeline aceita
qualquer implementação do Protocol sem mudar o orquestrador.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ml_pipeline.config import PipelineConfig
from ml_pipeline.pipeline import run


def test_pipeline_smoke_persiste_artefatos(tmp_path: Path) -> None:
    config = PipelineConfig(artifacts_dir=tmp_path, test_size=0.3, random_state=0)
    best = run(config)

    assert best.metrics.r2 > 0.5
    assert (tmp_path / "best_model.pkl").exists()
    assert (tmp_path / "metrics.json").exists()


def test_pipeline_aceita_persisters_injetados(tmp_path: Path) -> None:
    captured_models: list[tuple[Any, Path]] = []
    captured_metrics: list[tuple[dict[str, Any], Path]] = []

    class FakePersister:
        def save(self, model: Any, destination: Path) -> Path:
            captured_models.append((model, destination))
            return destination

    class FakeWriter:
        def write(self, payload: dict[str, Any], destination: Path) -> Path:
            captured_metrics.append((payload, destination))
            return destination

    config = PipelineConfig(artifacts_dir=tmp_path, test_size=0.3, random_state=0)
    run(config, model_persister=FakePersister(), metrics_writer=FakeWriter())

    assert len(captured_models) == 1
    assert captured_models[0][1] == tmp_path / "best_model.pkl"
    assert len(captured_metrics) == 1
    assert "best" in captured_metrics[0][0]
    assert "all" in captured_metrics[0][0]
    # Provar que não houve persistência real em disco para o modelo.
    assert not (tmp_path / "best_model.pkl").exists()
