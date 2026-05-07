"""Métricas de regressão.

Responsabilidade única: computar e formatar métricas. Não conhece
modelo, dados ou persistência.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


@dataclass(frozen=True)
class RegressionMetrics:
    """Carrier imutável de métricas de regressão."""

    rmse: float
    mae: float
    r2: float

    def to_dict(self) -> dict[str, float]:
        """Serializa as métricas como dicionário plano."""
        return asdict(self)


def compute_metrics(y_true: np.ndarray, y_pred: np.ndarray) -> RegressionMetrics:
    """Calcula RMSE, MAE e R² para um par (y_true, y_pred)."""
    return RegressionMetrics(
        rmse=float(np.sqrt(mean_squared_error(y_true, y_pred))),
        mae=float(mean_absolute_error(y_true, y_pred)),
        r2=float(r2_score(y_true, y_pred)),
    )
