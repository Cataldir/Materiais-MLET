"""Testes da CLI Typer."""

from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from ml_pipeline.cli import app

runner = CliRunner()


def test_cli_help_lista_flags() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "--test-size" in result.stdout
    assert "--random-state" in result.stdout
    assert "--artifacts-dir" in result.stdout


def test_cli_executa_pipeline_com_overrides(tmp_path: Path) -> None:
    result = runner.invoke(
        app,
        [
            "--artifacts-dir",
            str(tmp_path),
            "--test-size",
            "0.3",
            "--random-state",
            "0",
        ],
    )
    assert result.exit_code == 0, result.stdout
    assert "Best model:" in result.stdout
    assert (tmp_path / "best_model.pkl").exists()
    assert (tmp_path / "metrics.json").exists()
