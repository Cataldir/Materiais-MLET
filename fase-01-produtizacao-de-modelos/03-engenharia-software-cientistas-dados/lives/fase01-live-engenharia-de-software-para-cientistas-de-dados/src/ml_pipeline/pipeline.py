"""Orquestrador de alto nível.

SRP no topo: este módulo apenas coordena módulos especializados.
DIP: recebe os colaboradores ``ModelPersister`` e ``MetricsWriter`` por
injeção, em vez de instanciar implementações concretas.
"""

from __future__ import annotations

import logging
from typing import Any

import pandas as pd
from sklearn.model_selection import train_test_split

from ml_pipeline.config import PipelineConfig
from ml_pipeline.data import load_california_housing
from ml_pipeline.features import add_engineered_features
from ml_pipeline.persistence import (
    JsonMetricsWriter,
    MetricsWriter,
    ModelPersister,
    PickleModelPersister,
)
from ml_pipeline.preprocessing import clip_target_outliers
from ml_pipeline.training import TrainingResult, train_and_evaluate

logger = logging.getLogger(__name__)


def _split_features_target(
    df: pd.DataFrame, target_column: str
) -> tuple[pd.DataFrame, pd.Series]:
    return df.drop(columns=[target_column]), df[target_column]


def _build_metrics_payload(
    best: TrainingResult, all_results: list[TrainingResult]
) -> dict[str, Any]:
    return {
        "best": {"name": best.name, **best.metrics.to_dict()},
        "all": [
            {"name": r.name, **r.metrics.to_dict(), "fit_seconds": r.fit_seconds}
            for r in all_results
        ],
    }


def run(
    config: PipelineConfig,
    model_persister: ModelPersister | None = None,
    metrics_writer: MetricsWriter | None = None,
) -> TrainingResult:
    """Executa o pipeline completo e devolve o melhor modelo.

    Args:
        config: Configuração do pipeline.
        model_persister: Implementação de ``ModelPersister``. Se ``None``,
            usa ``PickleModelPersister``.
        metrics_writer: Implementação de ``MetricsWriter``. Se ``None``,
            usa ``JsonMetricsWriter``.

    Returns:
        O ``TrainingResult`` do melhor modelo (menor RMSE).
    """
    persister: ModelPersister = model_persister or PickleModelPersister()
    writer: MetricsWriter = metrics_writer or JsonMetricsWriter()

    raw = load_california_housing()
    cleaned = clip_target_outliers(raw, config.target_column, config.target_upper_clip)
    enriched = add_engineered_features(cleaned)

    features, target = _split_features_target(enriched, config.target_column)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.test_size,
        random_state=config.random_state,
    )

    results = train_and_evaluate(
        x_train, y_train, x_test, y_test, random_state=config.random_state
    )
    best = results[0]

    config.artifacts_dir.mkdir(parents=True, exist_ok=True)
    persister.save(best.estimator, config.artifacts_dir / "best_model.pkl")
    writer.write(
        _build_metrics_payload(best, results),
        config.artifacts_dir / "metrics.json",
    )

    logger.info("Melhor modelo: %s (RMSE=%.4f)", best.name, best.metrics.rmse)
    return best
