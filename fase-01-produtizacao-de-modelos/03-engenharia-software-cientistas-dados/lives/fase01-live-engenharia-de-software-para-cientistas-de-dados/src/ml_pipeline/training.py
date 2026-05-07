"""Treino e comparação de modelos.

Responsabilidade única: treinar cada estratégia registrada e produzir
métricas comparáveis. Não cuida de persistência nem de configuração.
"""

from __future__ import annotations

import logging
import time
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline

from ml_pipeline.evaluation import RegressionMetrics, compute_metrics
from ml_pipeline.models import MODEL_REGISTRY

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class TrainingResult:
    """Resultado de treino para um único modelo."""

    name: str
    estimator: Pipeline
    metrics: RegressionMetrics
    fit_seconds: float


def train_and_evaluate(
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    random_state: int,
) -> list[TrainingResult]:
    """Treina cada modelo registrado e devolve resultados ordenados por RMSE."""
    results: list[TrainingResult] = []
    for name, factory in MODEL_REGISTRY.items():
        estimator = factory(random_state=random_state)
        started = time.perf_counter()
        estimator.fit(x_train, y_train)
        elapsed = time.perf_counter() - started

        y_pred = np.asarray(estimator.predict(x_test))
        metrics = compute_metrics(np.asarray(y_test), y_pred)

        logger.info(
            "%s | RMSE=%.4f MAE=%.4f R2=%.4f (%.2fs)",
            name,
            metrics.rmse,
            metrics.mae,
            metrics.r2,
            elapsed,
        )
        results.append(TrainingResult(name, estimator, metrics, elapsed))

    return sorted(results, key=lambda r: r.metrics.rmse)
