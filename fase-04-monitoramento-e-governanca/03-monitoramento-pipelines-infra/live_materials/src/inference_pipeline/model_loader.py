"""
Carregamento de modelo do MLflow Model Registry.

Gerencia o ciclo de vida do modelo em memória, incluindo
versionamento e métricas de carregamento.
"""

import logging
import time

import mlflow
from mlflow.tracking import MlflowClient

from src.common.config import settings
from src.common.metrics import MODEL_VERSION_GAUGE

logger = logging.getLogger(__name__)


class ModelManager:
    """Gerencia carregamento e versionamento de modelos do MLflow."""

    def __init__(self):
        self.model = None
        self.model_version: str | None = None
        self.model_name: str = settings.MODEL_NAME
        self._client: MlflowClient | None = None

    @property
    def client(self) -> MlflowClient:
        if self._client is None:
            mlflow.set_tracking_uri(settings.MLFLOW_TRACKING_URI)
            self._client = MlflowClient()
        return self._client

    def load_model(self) -> None:
        """
        Carrega a versão mais recente do modelo do MLflow Registry.

        Tenta carregar do Model Registry. Se não houver modelo registrado,
        tenta carregar a última run do experimento.
        """
        start_time = time.time()
        logger.info("Carregando modelo '%s' do MLflow...", self.model_name)

        try:
            # Try loading from registry (latest version)
            model_uri = f"models:/{self.model_name}/latest"
            self.model = mlflow.sklearn.load_model(model_uri)

            # Get version info
            versions = self.client.get_latest_versions(self.model_name)
            if versions:
                self.model_version = versions[0].version
                MODEL_VERSION_GAUGE.labels(model_name=self.model_name).set(
                    int(self.model_version)
                )

            load_time = time.time() - start_time
            logger.info(
                "Modelo '%s' v%s carregado em %.2fs",
                self.model_name,
                self.model_version,
                load_time,
            )

        except Exception as e:
            logger.warning("Não foi possível carregar do Registry: %s", e)
            logger.info("Tentando carregar da última run...")
            self._load_from_latest_run()

    def _load_from_latest_run(self) -> None:
        """Fallback: carrega modelo da última run do experimento."""
        try:
            experiment = self.client.get_experiment_by_name(
                settings.MLFLOW_EXPERIMENT_NAME
            )
            if experiment is None:
                logger.error("Experimento '%s' não encontrado", settings.MLFLOW_EXPERIMENT_NAME)
                return

            runs = self.client.search_runs(
                experiment_ids=[experiment.experiment_id],
                order_by=["start_time DESC"],
                max_results=1,
            )

            if not runs:
                logger.error("Nenhuma run encontrada no experimento")
                return

            run_id = runs[0].info.run_id
            model_uri = f"runs:/{run_id}/model"
            self.model = mlflow.sklearn.load_model(model_uri)
            self.model_version = f"run-{run_id[:8]}"

            logger.info("Modelo carregado da run %s", run_id)

        except Exception as e:
            logger.error("Falha ao carregar modelo: %s", e)
            self.model = None

    def get_model_info(self) -> dict:
        """Retorna informações do modelo carregado."""
        return {
            "model_name": self.model_name,
            "model_version": self.model_version,
            "is_loaded": self.model is not None,
            "model_type": type(self.model).__name__ if self.model else None,
        }
