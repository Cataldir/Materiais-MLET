"""Facade para orquestrar o pipeline integrado em modo local-first."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

from src.pipeline_core import run_pipeline


def initialize_workspace(workspace: Path, source_dir: Path) -> None:
    """Copia os artefatos minimos para um workspace temporario."""

    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(source_dir / "data", workspace / "data")
    shutil.copy2(source_dir / "params.yaml", workspace / "params.yaml")


def run_demo_pipeline(workspace: Path | None = None) -> dict[str, object]:
    """Executa o pipeline no proprio pack ou em workspace isolado."""

    base_dir = Path(__file__).resolve().parent
    if workspace is None:
        return run_pipeline(base_dir)
    initialize_workspace(workspace, base_dir)
    return run_pipeline(workspace)


if __name__ == "__main__":
    print(json.dumps(run_demo_pipeline(), indent=2, ensure_ascii=False))