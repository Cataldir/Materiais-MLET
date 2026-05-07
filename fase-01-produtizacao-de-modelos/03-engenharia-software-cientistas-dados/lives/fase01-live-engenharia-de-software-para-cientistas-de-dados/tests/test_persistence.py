"""Testes da camada de persistência.

Demonstram DIP/LSP: o pipeline pode receber qualquer implementação que
satisfaça os Protocols ``ModelPersister`` e ``MetricsWriter``.
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any

from ml_pipeline.persistence import (
    JsonMetricsWriter,
    MetricsWriter,
    ModelPersister,
    PickleModelPersister,
)


class _InMemoryPersister:
    """Implementação alternativa que não toca disco — prova LSP."""

    def __init__(self) -> None:
        self.saved: list[tuple[Any, Path]] = []

    def save(self, model: Any, destination: Path) -> Path:
        self.saved.append((model, destination))
        return destination


class _InMemoryWriter:
    def __init__(self) -> None:
        self.payloads: list[tuple[dict[str, Any], Path]] = []

    def write(self, payload: dict[str, Any], destination: Path) -> Path:
        self.payloads.append((payload, destination))
        return destination


def test_pickle_persister_round_trip(tmp_path: Path) -> None:
    persister = PickleModelPersister()
    target = tmp_path / "nested" / "model.pkl"
    payload = {"a": 1, "b": [1, 2, 3]}

    written = persister.save(payload, target)

    assert written == target
    assert target.exists()
    with target.open("rb") as handle:
        assert pickle.load(handle) == payload


def test_json_writer_grava_payload_valido(tmp_path: Path) -> None:
    writer = JsonMetricsWriter()
    target = tmp_path / "metrics.json"
    payload: dict[str, Any] = {"best": {"name": "ridge", "rmse": 0.5}}

    written = writer.write(payload, target)

    assert written == target
    assert json.loads(target.read_text()) == payload


def test_in_memory_implementations_satisfazem_protocolos() -> None:
    persister: ModelPersister = _InMemoryPersister()
    writer: MetricsWriter = _InMemoryWriter()

    persister.save("modelo", Path("/tmp/x"))
    writer.write({"k": 1}, Path("/tmp/y"))

    assert persister.saved == [("modelo", Path("/tmp/x"))]  # type: ignore[attr-defined]
    assert writer.payloads == [({"k": 1}, Path("/tmp/y"))]  # type: ignore[attr-defined]
