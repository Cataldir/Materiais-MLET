"""Adapter e Facade para integrar sklearn e tracking com fallback local."""

from __future__ import annotations

import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42


@dataclass(frozen=True, slots=True)
class TrainingSummary:
    """Resumo da execucao do pipeline com tracking."""

    tracker_name: str
    run_id: str
    accuracy: float
    feature_count: int
    params: dict[str, object]
    metrics: dict[str, float]


@dataclass(slots=True)
class InMemoryTrackingAdapter:
    """Adapter local para tracking quando MLflow nao esta disponivel."""

    tracker_name: str = "in_memory"
    runs: dict[str, dict[str, object]] = field(default_factory=dict)

    def start_run(self) -> str:
        run_id = uuid.uuid4().hex[:8]
        self.runs[run_id] = {"params": {}, "metrics": {}}
        return run_id

    def log_param(self, run_id: str, name: str, value: object) -> None:
        self.runs[run_id]["params"][name] = value

    def log_metric(self, run_id: str, name: str, value: float) -> None:
        self.runs[run_id]["metrics"][name] = value

    def get_run_payload(self, run_id: str) -> dict[str, object]:
        return self.runs[run_id]


@dataclass(slots=True)
class MlflowTrackingAdapter:
    """Adapter opcional para MLflow, criado apenas se a dependencia existir."""

    tracking_uri: str
    tracker_name: str = "mlflow"

    def __post_init__(self) -> None:
        import mlflow

        self._mlflow = mlflow
        self._mlflow.set_tracking_uri(self.tracking_uri)

    def start_run(self) -> str:
        run = self._mlflow.start_run()
        return run.info.run_id

    def log_param(self, run_id: str, name: str, value: object) -> None:
        self._mlflow.log_param(name, value)

    def log_metric(self, run_id: str, name: str, value: float) -> None:
        self._mlflow.log_metric(name, value)

    def get_run_payload(self, run_id: str) -> dict[str, object]:
        return {"params": {}, "metrics": {}}


def build_tracker(prefer_mlflow: bool = True, tracking_uri: str | None = None) -> object:
    """Cria o tracker preferido ou faz fallback para memoria."""

    if prefer_mlflow:
        try:
            uri = tracking_uri or str(Path("mlruns").resolve())
            return MlflowTrackingAdapter(tracking_uri=uri)
        except ModuleNotFoundError:
            LOGGER.info("mlflow nao encontrado; usando tracker em memoria")
    return InMemoryTrackingAdapter()


def train_pipeline() -> tuple[float, int]:
    """Treina um pipeline sklearn pequeno e retorna accuracy e numero de features."""

    features, target = load_breast_cancer(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=target,
    )
    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("model", LogisticRegression(max_iter=500, random_state=RANDOM_STATE)),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)
    return accuracy_score(y_test, predictions), x_train.shape[1]


def run_sdk_pipeline(
    prefer_mlflow: bool = True,
    tracking_uri: str | None = None,
) -> TrainingSummary:
    """Facade do pipeline com treino, tracking e resumo final."""

    tracker = build_tracker(prefer_mlflow=prefer_mlflow, tracking_uri=tracking_uri)
    run_id = tracker.start_run()
    accuracy, feature_count = train_pipeline()
    tracker.log_param(run_id, "model", "logistic_regression")
    tracker.log_param(run_id, "random_state", RANDOM_STATE)
    tracker.log_metric(run_id, "accuracy", accuracy)
    payload = tracker.get_run_payload(run_id)
    return TrainingSummary(
        tracker_name=tracker.tracker_name,
        run_id=run_id,
        accuracy=accuracy,
        feature_count=feature_count,
        params=dict(payload.get("params", {})),
        metrics={"accuracy": accuracy, **dict(payload.get("metrics", {}))},
    )


def main() -> None:
    """Executa o pipeline e imprime o resumo do tracking."""

    summary = run_sdk_pipeline(prefer_mlflow=True)
    LOGGER.info(
        "tracker=%s run_id=%s accuracy=%.3f features=%d",
        summary.tracker_name,
        summary.run_id,
        summary.accuracy,
        summary.feature_count,
    )


if __name__ == "__main__":
    main()