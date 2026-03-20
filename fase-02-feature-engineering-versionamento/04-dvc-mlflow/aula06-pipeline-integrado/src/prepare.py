"""Executa a etapa de preparo do pipeline integrado."""

from __future__ import annotations

from pathlib import Path

from src.pipeline_core import prepare_dataset

if __name__ == "__main__":
    prepare_dataset(Path(__file__).resolve().parents[1])