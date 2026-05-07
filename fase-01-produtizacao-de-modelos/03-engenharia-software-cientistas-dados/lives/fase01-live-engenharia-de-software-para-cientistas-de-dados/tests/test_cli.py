"""Teste da CLI."""

from typer.testing import CliRunner

from ml_pipeline.cli import app


def test_cli_help():
    result = CliRunner().invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "test-size" in result.stdout
