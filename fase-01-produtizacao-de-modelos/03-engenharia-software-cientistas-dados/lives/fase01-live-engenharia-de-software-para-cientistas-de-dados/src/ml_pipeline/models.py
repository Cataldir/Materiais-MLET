"""Modelos e avaliação (SRP: definir e treinar modelos)."""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def _wrap(estimator):
    """Coloca scaler + estimador num Pipeline (evita data leakage)."""
    return Pipeline([("scaler", StandardScaler()), ("model", estimator)])


def build_models(random_state: int) -> dict:
    """Registry de modelos. Adicionar um modelo = uma linha aqui."""
    return {
        "linear_regression": _wrap(LinearRegression()),
        "ridge": _wrap(Ridge(alpha=1.0)),
        "lasso": _wrap(Lasso(alpha=0.001)),
        "random_forest": _wrap(
            RandomForestRegressor(
                n_estimators=200, random_state=random_state, n_jobs=-1
            )
        ),
        "mlp": _wrap(
            MLPRegressor(
                hidden_layer_sizes=(100,), max_iter=500, random_state=random_state
            )
        ),
    }


def evaluate(y_true, y_pred) -> dict:
    """Calcula RMSE, MAE e R²."""
    return {
        "rmse": float(np.sqrt(mean_squared_error(y_true, y_pred))),
        "mae": float(mean_absolute_error(y_true, y_pred)),
        "r2": float(r2_score(y_true, y_pred)),
    }


def train_and_evaluate(x_train, y_train, x_test, y_test, random_state: int) -> list:
    """Treina todos os modelos e devolve lista ordenada por RMSE crescente."""
    results = []
    for name, model in build_models(random_state).items():
        model.fit(x_train, y_train)
        metrics = evaluate(y_test, model.predict(x_test))
        results.append({"name": name, "model": model, **metrics})
    return sorted(results, key=lambda r: r["rmse"])
