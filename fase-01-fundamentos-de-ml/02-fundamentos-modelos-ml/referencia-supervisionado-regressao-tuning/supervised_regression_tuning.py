"""Referencia canonica de regressao e tuning para a fase 01.

Uso:
    python supervised_regression_tuning.py
"""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42
TEST_SIZE = 0.2
ENABLE_DEBUG_BREAKPOINT = False


@dataclass(frozen=True)
class RegressionSummary:
    baseline_rmse: float
    ridge_rmse: float
    tuned_random_forest_rmse: float
    baseline_r2: float
    ridge_r2: float
    tuned_random_forest_r2: float
    best_model: str
    best_params: dict[str, int | float | str]
    top_features: list[str]


def _rmse(y_true: pd.Series, y_pred: np.ndarray) -> float:
    return float(np.sqrt(mean_squared_error(y_true, y_pred)))


def build_dataset() -> tuple[pd.DataFrame, pd.Series]:
    dataset = fetch_california_housing(as_frame=True)
    return dataset.data, dataset.target


def train_reference_models(debug: bool = False) -> RegressionSummary:
    features, target = build_dataset()
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
    )

    if debug:
        breakpoint()

    linear_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", LinearRegression()),
        ]
    )
    linear_pipeline.fit(x_train, y_train)
    baseline_predictions = linear_pipeline.predict(x_test)

    ridge_pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("regressor", Ridge(alpha=1.0)),
        ]
    )
    ridge_pipeline.fit(x_train, y_train)
    ridge_predictions = ridge_pipeline.predict(x_test)

    search = GridSearchCV(
        estimator=RandomForestRegressor(random_state=RANDOM_STATE),
        param_grid={
            "n_estimators": [80, 120],
            "max_depth": [None, 10],
            "min_samples_leaf": [1, 3],
        },
        cv=3,
        n_jobs=1,
        scoring="neg_root_mean_squared_error",
    )
    search.fit(x_train, y_train)
    tuned_model = search.best_estimator_
    tuned_predictions = tuned_model.predict(x_test)

    importances = pd.Series(tuned_model.feature_importances_, index=features.columns)
    best_scores = {
        "linear_regression": _rmse(y_test, baseline_predictions),
        "ridge": _rmse(y_test, ridge_predictions),
        "random_forest_tuned": _rmse(y_test, tuned_predictions),
    }
    best_model = min(best_scores, key=best_scores.get)

    return RegressionSummary(
        baseline_rmse=best_scores["linear_regression"],
        ridge_rmse=best_scores["ridge"],
        tuned_random_forest_rmse=best_scores["random_forest_tuned"],
        baseline_r2=float(r2_score(y_test, baseline_predictions)),
        ridge_r2=float(r2_score(y_test, ridge_predictions)),
        tuned_random_forest_r2=float(r2_score(y_test, tuned_predictions)),
        best_model=best_model,
        best_params={key: value for key, value in search.best_params_.items()},
        top_features=importances.sort_values(ascending=False).head(3).index.tolist(),
    )


def run_reference_demo(debug: bool = False) -> dict[str, object]:
    summary = train_reference_models(debug=debug)
    return asdict(summary)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_reference_demo(debug=ENABLE_DEBUG_BREAKPOINT)
    LOGGER.info("Melhor modelo: %s", summary["best_model"])
    LOGGER.info(
        "RMSE -> linear=%.3f | ridge=%.3f | tuned_rf=%.3f",
        summary["baseline_rmse"],
        summary["ridge_rmse"],
        summary["tuned_random_forest_rmse"],
    )
    LOGGER.info("Top atributos: %s", ", ".join(summary["top_features"]))
    LOGGER.info("Melhores hiperparametros: %s", summary["best_params"])


if __name__ == "__main__":
    main()