"""Executa a etapa de treino do pipeline integrado."""

from __future__ import annotations

from pathlib import Path

from src.pipeline_core import train_model

if __name__ == "__main__":
    train_model(Path(__file__).resolve().parents[1])