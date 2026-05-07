"""Entry point CLI baseado em Typer.

Atende ao requisito ``CLI com Pydantic Settings``: as flags da CLI
sobrescrevem os defaults definidos em ``PipelineConfig`` (que por sua vez
podem vir de variáveis de ambiente ``MLPIPE_*``).
"""

from __future__ import annotations

import logging
from pathlib import Path

import typer

from ml_pipeline.config import PipelineConfig
from ml_pipeline.pipeline import run

app = typer.Typer(
    add_completion=False,
    help="Pipeline de regressão California Housing.",
    invoke_without_command=True,
    no_args_is_help=False,
)


@app.callback()
def main(
    ctx: typer.Context,
    artifacts_dir: Path | None = typer.Option(None, help="Diretório dos artefatos."),  # noqa: B008
    target_column: str | None = typer.Option(None, help="Nome da coluna alvo."),  # noqa: B008
    target_upper_clip: float | None = typer.Option(  # noqa: B008
        None, help="Limite superior do alvo."
    ),
    test_size: float | None = typer.Option(None, help="Proporção do teste (0,1)."),  # noqa: B008
    random_state: int | None = typer.Option(None, help="Semente de aleatoriedade."),  # noqa: B008
) -> None:
    """Treina, avalia e persiste o melhor modelo.

    Flags fornecidas sobrescrevem os defaults de ``PipelineConfig``.
    Variáveis de ambiente ``MLPIPE_*`` continuam valendo como defaults.
    """
    if ctx.invoked_subcommand is not None:
        return

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )

    overrides = {
        "artifacts_dir": artifacts_dir,
        "target_column": target_column,
        "target_upper_clip": target_upper_clip,
        "test_size": test_size,
        "random_state": random_state,
    }
    overrides = {key: value for key, value in overrides.items() if value is not None}

    config = PipelineConfig(**overrides)
    result = run(config)
    typer.echo(
        f"Best model: {result.name} | RMSE={result.metrics.rmse:.4f} "
        f"MAE={result.metrics.mae:.4f} R2={result.metrics.r2:.4f}"
    )


if __name__ == "__main__":
    app()
