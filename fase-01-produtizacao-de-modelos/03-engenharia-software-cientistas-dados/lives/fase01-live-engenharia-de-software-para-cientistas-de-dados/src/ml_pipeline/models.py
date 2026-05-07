"""Catálogo de modelos.

Aplica o padrão Strategy: cada modelo é construído por uma factory
intercambiável que respeita o protocolo ``RegressorFactory``. Cobre o
princípio Open/Closed do SOLID — adicionar um novo modelo só exige
registrar uma nova factory em ``MODEL_REGISTRY``, sem alterar o
orquestrador.

O ``StandardScaler`` vive dentro do ``sklearn.pipeline.Pipeline``, o que
elimina o data leakage exibido propositalmente no notebook messy.
"""

from __future__ import annotations

from typing import Protocol

from sklearn.base import RegressorMixin
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


class RegressorFactory(Protocol):
    """Protocolo estrutural para fábricas de regressores."""

    def __call__(self, random_state: int) -> Pipeline:
        """Constrói um Pipeline ``(scaler, estimator)`` parametrizado."""


def _wrap_with_scaler(estimator: RegressorMixin) -> Pipeline:
    """Encapsula o estimador em um Pipeline com ``StandardScaler``."""
    return Pipeline(steps=[("scaler", StandardScaler()), ("estimator", estimator)])


def build_linear_regression(random_state: int) -> Pipeline:
    """Linear Regression sem hiperparâmetros estocásticos."""
    del random_state
    return _wrap_with_scaler(LinearRegression())


def build_ridge(random_state: int) -> Pipeline:
    """Ridge regression com regularização L2."""
    return _wrap_with_scaler(Ridge(alpha=1.0, random_state=random_state))


def build_lasso(random_state: int) -> Pipeline:
    """Lasso regression com regularização L1."""
    return _wrap_with_scaler(Lasso(alpha=0.001, random_state=random_state))


def build_random_forest(random_state: int) -> Pipeline:
    """Random Forest com 200 árvores."""
    return _wrap_with_scaler(
        RandomForestRegressor(n_estimators=200, random_state=random_state, n_jobs=-1)
    )


def build_gradient_boosting(random_state: int) -> Pipeline:
    """Gradient Boosting com 200 estimadores."""
    return _wrap_with_scaler(
        GradientBoostingRegressor(n_estimators=200, random_state=random_state)
    )


MODEL_REGISTRY: dict[str, RegressorFactory] = {
    "linear_regression": build_linear_regression,
    "ridge": build_ridge,
    "lasso": build_lasso,
    "random_forest": build_random_forest,
    "gradient_boosting": build_gradient_boosting,
}
