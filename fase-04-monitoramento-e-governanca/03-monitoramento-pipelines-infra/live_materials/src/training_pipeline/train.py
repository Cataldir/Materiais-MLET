"""
Pipeline de treinamento observável com MLflow + Prometheus.

Demonstra instrumentação completa de um pipeline de treino
usando scikit-learn, exportando métricas para Prometheus
e registrando experimentos no MLflow.
"""

import logging
import time
from pathlib import Path

import mlflow
import mlflow.sklearn
import numpy as np
from prometheus_client import start_http_server
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from src.common.config import settings
from src.common.metrics import (
    TRAINING_EPOCH_ACCURACY,
    TRAINING_EPOCH_DURATION,
    TRAINING_EPOCH_LOSS,
    TRAINING_SAMPLES_PROCESSED,
    TRAINING_TOTAL_DURATION,
)

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)


def load_and_split_data(test_size: float = 0.2, random_state: int = 42):
    """Carrega dataset Iris e divide em treino/teste."""
    data = load_iris()
    X_train, X_test, y_train, y_test = train_test_split(
        data.data, data.target, test_size=test_size, random_state=random_state
    )
    logger.info(
        "Dataset carregado: %d treino, %d teste, %d features",
        len(X_train),
        len(X_test),
        X_train.shape[1],
    )
    return X_train, X_test, y_train, y_test, data.feature_names, data.target_names


def save_reference_data(X_train: np.ndarray, feature_names: list[str]):
    """Salva dados de referência para detecção de drift posterior."""
    ref_path = Path(settings.REFERENCE_DATA_PATH)
    ref_path.parent.mkdir(parents=True, exist_ok=True)
    np.savez(ref_path, data=X_train, feature_names=np.array(feature_names))
    logger.info("Dados de referência salvos em %s", ref_path)


def train_incremental(
    X_train: np.ndarray,
    y_train: np.ndarray,
    n_estimators_steps: list[int],
    experiment_name: str,
):
    """
    Treina modelo RandomForest incrementalmente, simulando epochs.

    Cada step adiciona mais estimadores e emite métricas como se fosse uma
    epoch, permitindo visualizar o progresso no Grafana em tempo real.
    """
    model = None
    for step, n_est in enumerate(n_estimators_steps):
        step_start = time.time()

        model = RandomForestClassifier(
            n_estimators=n_est,
            random_state=42,
            warm_start=True if step > 0 else False,
        )
        # Rebuild with warm_start=True to reuse previous trees
        if step > 0:
            model.n_estimators = n_est
            model.warm_start = True

        model = RandomForestClassifier(n_estimators=n_est, random_state=42)
        model.fit(X_train, y_train)

        train_acc = model.score(X_train, y_train)
        train_loss = 1.0 - train_acc  # pseudo-loss for demonstration

        step_duration = time.time() - step_start

        # Emit Prometheus metrics
        TRAINING_EPOCH_LOSS.labels(experiment_name=experiment_name).set(train_loss)
        TRAINING_EPOCH_ACCURACY.labels(experiment_name=experiment_name).set(train_acc)
        TRAINING_EPOCH_DURATION.labels(experiment_name=experiment_name).observe(step_duration)
        TRAINING_SAMPLES_PROCESSED.labels(experiment_name=experiment_name).inc(len(X_train))

        # Log to MLflow
        mlflow.log_metric("train_loss", train_loss, step=step)
        mlflow.log_metric("train_accuracy", train_acc, step=step)
        mlflow.log_metric("n_estimators", n_est, step=step)

        logger.info(
            "Step %d/%d — n_estimators=%d, acc=%.4f, loss=%.4f, duration=%.2fs",
            step + 1,
            len(n_estimators_steps),
            n_est,
            train_acc,
            train_loss,
            step_duration,
        )

        # Small delay so Prometheus can scrape intermediate values
        time.sleep(2)

    return model


def evaluate_model(model, X_test, y_test, target_names):
    """Avalia o modelo e retorna dicionário de métricas."""
    y_pred = model.predict(X_test)
    metrics = {
        "test_accuracy": accuracy_score(y_test, y_pred),
        "test_f1_macro": f1_score(y_test, y_pred, average="macro"),
        "test_precision_macro": precision_score(y_test, y_pred, average="macro"),
        "test_recall_macro": recall_score(y_test, y_pred, average="macro"),
    }
    logger.info("Avaliação: %s", metrics)
    return metrics


def run_training_pipeline():
    """Executa o pipeline completo de treino."""

    # Start Prometheus metrics server
    start_http_server(settings.PROMETHEUS_PORT)
    logger.info("Prometheus metrics server em :%d", settings.PROMETHEUS_PORT)

    # Configure MLflow
    mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
    mlflow.set_experiment(settings.MLFLOW_EXPERIMENT_NAME)

    experiment_name = settings.MLFLOW_EXPERIMENT_NAME

    with mlflow.start_run(run_name=f"training-{int(time.time())}"):
        total_start = time.time()

        # 1. Load data
        X_train, X_test, y_train, y_test, feature_names, target_names = (
            load_and_split_data()
        )

        mlflow.log_param("dataset", "iris")
        mlflow.log_param("train_size", len(X_train))
        mlflow.log_param("test_size", len(X_test))
        mlflow.log_param("n_features", X_train.shape[1])

        # 2. Save reference data for drift detection
        save_reference_data(X_train, list(feature_names))

        # 3. Train incrementally (simulating epochs)
        n_estimators_steps = [10, 25, 50, 75, 100, 150, 200]
        mlflow.log_param("n_estimators_steps", str(n_estimators_steps))

        model = train_incremental(X_train, y_train, n_estimators_steps, experiment_name)

        # 4. Evaluate
        metrics = evaluate_model(model, X_test, y_test, target_names)
        for name, value in metrics.items():
            mlflow.log_metric(name, value)

        # 5. Log model to MLflow
        mlflow.sklearn.log_model(
            model,
            "model",
            registered_model_name=settings.MODEL_NAME,
        )

        total_duration = time.time() - total_start
        TRAINING_TOTAL_DURATION.observe(total_duration)
        mlflow.log_metric("total_duration_seconds", total_duration)

        logger.info("Pipeline de treino concluído em %.2fs", total_duration)
        logger.info("Modelo registrado como '%s'", settings.MODEL_NAME)

    # Keep process alive for Prometheus scraping
    logger.info("Treino finalizado. Mantendo métricas disponíveis para scraping...")
    try:
        while True:
            time.sleep(30)
    except KeyboardInterrupt:
        logger.info("Encerrando.")


if __name__ == "__main__":
    run_training_pipeline()
