"""Pipeline sklearn — transformadores custom, grid search e model card.

Demonstra construção de pipelines robustos com transformadores personalizados
e busca de hiperparâmetros estruturada.

Uso:
    python pipeline_sklearn.py
"""

import logging

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.datasets import fetch_california_housing
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ITER_SEARCH = 20
CV_FOLDS = 5


class OutlierClipper(BaseEstimator, TransformerMixin):
    """Transformador que limita outliers via percentil.

    Attributes:
        lower_percentile: Percentil inferior de clipping.
        upper_percentile: Percentil superior de clipping.
        lower_bounds_: Limites inferiores por feature (após fit).
        upper_bounds_: Limites superiores por feature (após fit).
    """

    def __init__(self, lower_percentile: float = 1.0, upper_percentile: float = 99.0) -> None:
        """Inicializa o clipper de outliers.

        Args:
            lower_percentile: Percentil inferior (0-100).
            upper_percentile: Percentil superior (0-100).
        """
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.lower_bounds_: np.ndarray | None = None
        self.upper_bounds_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> "OutlierClipper":
        """Calcula os limites de clipping.

        Args:
            X: Dados de treino.
            y: Ignorado (compatibilidade com sklearn).

        Returns:
            Self.
        """
        self.lower_bounds_ = np.percentile(X, self.lower_percentile, axis=0)
        self.upper_bounds_ = np.percentile(X, self.upper_percentile, axis=0)
        return self

    def transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Aplica clipping nos dados.

        Args:
            X: Dados a transformar.
            y: Ignorado (compatibilidade com sklearn).

        Returns:
            Dados com outliers limitados.
        """
        if self.lower_bounds_ is None or self.upper_bounds_ is None:
            raise ValueError("Transformer not fitted yet. Call fit() first.")
        return np.clip(X, self.lower_bounds_, self.upper_bounds_)


def build_pipeline() -> Pipeline:
    """Constrói pipeline com transformadores custom e Random Forest.

    Returns:
        Pipeline sklearn configurado.
    """
    return Pipeline([
        ("clipper", OutlierClipper()),
        ("scaler", StandardScaler()),
        ("model", RandomForestRegressor(random_state=RANDOM_STATE)),
    ])


def run_random_search(pipeline: Pipeline, X_train: np.ndarray, y_train: np.ndarray) -> Pipeline:
    """Executa RandomizedSearchCV para otimização de hiperparâmetros.

    Args:
        pipeline: Pipeline base a ser otimizado.
        X_train: Features de treino.
        y_train: Target de treino.

    Returns:
        Melhor pipeline encontrado.
    """
    param_dist = {
        "model__n_estimators": [50, 100, 200, 300],
        "model__max_depth": [None, 5, 10, 15, 20],
        "model__min_samples_split": [2, 5, 10],
        "model__min_samples_leaf": [1, 2, 4],
        "clipper__lower_percentile": [1.0, 5.0],
        "clipper__upper_percentile": [95.0, 99.0],
    }
    search = RandomizedSearchCV(
        pipeline,
        param_distributions=param_dist,
        n_iter=N_ITER_SEARCH,
        cv=CV_FOLDS,
        scoring="r2",
        random_state=RANDOM_STATE,
        n_jobs=-1,
        verbose=1,
    )
    search.fit(X_train, y_train)
    logger.info("Melhores parâmetros: %s", search.best_params_)
    logger.info("Melhor R² (CV): %.4f", search.best_score_)
    return search.best_estimator_


def evaluate(pipeline: Pipeline, X_test: np.ndarray, y_test: np.ndarray) -> dict[str, float]:
    """Avalia o pipeline no conjunto de teste.

    Args:
        pipeline: Pipeline treinado.
        X_test: Features de teste.
        y_test: Target de teste.

    Returns:
        Dicionário com métricas de avaliação.
    """
    y_pred = pipeline.predict(X_test)
    metrics = {
        "r2": float(r2_score(y_test, y_pred)),
        "mae": float(mean_absolute_error(y_test, y_pred)),
        "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
    }
    logger.info("R²:   %.4f", metrics["r2"])
    logger.info("MAE:  %.4f", metrics["mae"])
    logger.info("RMSE: %.4f", metrics["rmse"])
    return metrics


def main() -> None:
    """Executa pipeline completo de treino e avaliação."""
    housing = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(
        housing.data, housing.target,
        test_size=TEST_SIZE, random_state=RANDOM_STATE,
    )
    logger.info("Dataset: %d features | Treino: %d | Teste: %d",
                X_train.shape[1], len(X_train), len(X_test))

    pipeline = build_pipeline()
    best_pipeline = run_random_search(pipeline, X_train, y_train)
    evaluate(best_pipeline, X_test, y_test)


if __name__ == "__main__":
    main()
