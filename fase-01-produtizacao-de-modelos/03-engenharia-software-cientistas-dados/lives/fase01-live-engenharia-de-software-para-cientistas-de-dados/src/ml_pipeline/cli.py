"""CLI do pipeline (Typer + Pydantic Settings)."""

import typer

from ml_pipeline.config import PipelineConfig
from ml_pipeline.pipeline import run

app = typer.Typer(add_completion=False, help="Pipeline California Housing.")


@app.command()
def main(
    test_size: float = 0.2,
    random_state: int = 42,
) -> None:
    """Treina, avalia e salva o melhor modelo em ./artifacts/."""
    config = PipelineConfig(test_size=test_size, random_state=random_state)
    best = run(config)
    typer.echo(
        f"Best: {best['name']} | RMSE={best['rmse']:.4f} "
        f"MAE={best['mae']:.4f} R2={best['r2']:.4f}"
    )


if __name__ == "__main__":
    app()
