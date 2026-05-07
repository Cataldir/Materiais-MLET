"""Persistência de artefatos.

Aplica três princípios SOLID em uma única peça:

- **ISP** (Interface Segregation): dois protocolos pequenos
  (``ModelPersister`` e ``MetricsWriter``) em vez de um protocolo gordo.
- **DIP** (Dependency Inversion): o orquestrador em ``pipeline.py``
  depende destes Protocols, não de ``pickle``/``json`` diretamente.
- **LSP** (Liskov Substitution): qualquer implementação que satisfaça os
  protocolos pode ser injetada sem quebrar o pipeline (ver
  ``tests/test_persistence.py``).
"""

from __future__ import annotations

import json
import pickle
from pathlib import Path
from typing import Any, Protocol


class ModelPersister(Protocol):
    """Persiste um modelo treinado em disco."""

    def save(self, model: Any, destination: Path) -> Path:
        """Serializa ``model`` em ``destination`` e devolve o caminho."""


class MetricsWriter(Protocol):
    """Escreve um payload de métricas em disco."""

    def write(self, payload: dict[str, Any], destination: Path) -> Path:
        """Grava ``payload`` em ``destination`` e devolve o caminho."""


class PickleModelPersister:
    """Implementação padrão baseada em ``pickle``."""

    def save(self, model: Any, destination: Path) -> Path:
        """Serializa ``model`` em ``destination`` usando pickle."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("wb") as handle:
            pickle.dump(model, handle)
        return destination


class JsonMetricsWriter:
    """Implementação padrão baseada em JSON indentado."""

    def write(self, payload: dict[str, Any], destination: Path) -> Path:
        """Serializa ``payload`` em ``destination`` como JSON."""
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(json.dumps(payload, indent=2))
        return destination
