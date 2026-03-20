"""Executa a etapa de avaliacao do pipeline integrado."""

from __future__ import annotations

from pathlib import Path

from src.pipeline_core import evaluate_model

if __name__ == "__main__":
    evaluate_model(Path(__file__).resolve().parents[1])