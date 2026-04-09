"""Configuração centralizada via variáveis de ambiente."""

import os


class Settings:
    """Configurações do projeto carregadas de variáveis de ambiente."""

    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MLFLOW_EXPERIMENT_NAME: str = os.getenv("MLFLOW_EXPERIMENT_NAME", "ml-pipeline-monitoring")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "iris-classifier")
    MODEL_STAGE: str = os.getenv("MODEL_STAGE", "Production")

    PROMETHEUS_PORT: int = int(os.getenv("PROMETHEUS_PORT", "8001"))

    INFERENCE_HOST: str = os.getenv("INFERENCE_HOST", "0.0.0.0")
    INFERENCE_PORT: int = int(os.getenv("INFERENCE_PORT", "8000"))

    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Drift detection
    DRIFT_THRESHOLD: float = float(os.getenv("DRIFT_THRESHOLD", "0.1"))
    DRIFT_CHECK_INTERVAL: int = int(os.getenv("DRIFT_CHECK_INTERVAL", "300"))

    # Reference data path (saved from training)
    REFERENCE_DATA_PATH: str = os.getenv("REFERENCE_DATA_PATH", "data/reference.npz")


settings = Settings()
