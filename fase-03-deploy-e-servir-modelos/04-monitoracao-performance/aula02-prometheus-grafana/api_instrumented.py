"""FastAPI instrumentada com Prometheus — métricas de latência e predições.

Demonstra como adicionar observabilidade a uma API de ML usando
prometheus-client para métricas de negócio e sistema.

Uso:
    uvicorn api_instrumented:app --host 0.0.0.0 --port 8000
    # Métricas disponíveis em http://localhost:8000/metrics
"""

import logging
import time
from dataclasses import asdict, dataclass
from typing import Any

import numpy as np
from fastapi import FastAPI, Request, Response
from pydantic import BaseModel

try:
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
except ImportError:  # pragma: no cover - fallback only used in lean environments.
    load_iris = None
    RandomForestClassifier = Any

try:
    from prometheus_client import (
        CONTENT_TYPE_LATEST,
        Counter,
        Gauge,
        Histogram,
        generate_latest,
    )

    counter_factory = Counter
    gauge_factory = Gauge
    histogram_factory = Histogram
except ImportError:  # pragma: no cover - fallback only used in lean environments.
    CONTENT_TYPE_LATEST = "text/plain; version=0.0.4; charset=utf-8"

    class _NullMetric:
        def labels(self, **_: str) -> "_NullMetric":
            return self

        def observe(self, _: float) -> None:
            return None

        def inc(self) -> None:
            return None

        def dec(self) -> None:
            return None

    def counter_factory(*_: object, **__: object) -> _NullMetric:
        return _NullMetric()

    def gauge_factory(*_: object, **__: object) -> _NullMetric:
        return _NullMetric()

    def histogram_factory(*_: object, **__: object) -> _NullMetric:
        return _NullMetric()

    def generate_latest() -> bytes:
        return b"# prometheus_client not installed\n"


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PREDICTION_COUNTER = counter_factory(
    "ml_predictions_total",
    "Total de predições realizadas",
    ["endpoint", "predicted_class", "status"],
)
PREDICTION_LATENCY = histogram_factory(
    "ml_prediction_latency_seconds",
    "Latência das predições em segundos",
    ["endpoint"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)
MODEL_CONFIDENCE = histogram_factory(
    "ml_prediction_confidence",
    "Distribuição de confiança das predições",
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0],
)
ACTIVE_REQUESTS = gauge_factory(
    "ml_active_requests",
    "Número de requisições ativas",
    ["endpoint"],
)

app = FastAPI(title="ML API com Prometheus", version="1.0.0")

_model: RandomForestClassifier | None = None


@dataclass(frozen=True, slots=True)
class PredictionResult:
    """Representa uma resposta de predicao testavel fora da API."""

    predicted_class: int
    confidence: float


def get_model() -> RandomForestClassifier:
    """Carrega ou retorna modelo em cache.

    Returns:
        Modelo treinado.
    """
    global _model
    if load_iris is None:
        return None
    if _model is None:
        feature_matrix, target_vector = load_iris(return_X_y=True)
        _model = RandomForestClassifier(n_estimators=50, random_state=42)
        _model.fit(feature_matrix, target_vector)
    return _model


def score_features_fallback(features: list[float]) -> PredictionResult:
    """Produz uma predicao local simples quando sklearn nao esta disponivel."""
    sepal_length, sepal_width, petal_length, petal_width = features
    if petal_length < 2.5:
        predicted_class = 0
        confidence = 0.98
    elif petal_width < 1.8:
        predicted_class = 1
        confidence = 0.84 + min(0.10, max(0.0, (petal_length - 3.0) / 20))
    else:
        predicted_class = 2
        confidence = 0.86 + min(
            0.10,
            max(0.0, (sepal_length + petal_width - sepal_width) / 20),
        )
    return PredictionResult(
        predicted_class=predicted_class,
        confidence=float(min(confidence, 0.99)),
    )


class PredictRequest(BaseModel):
    """Schema de entrada para predição."""

    features: list[float]


def score_features(
    features: list[float],
    model: RandomForestClassifier | None = None,
) -> PredictionResult:
    """Executa o core de scoring para reuso em testes e notebooks."""
    if len(features) != 4:
        raise ValueError("Iris model expects exactly 4 numeric features")
    active_model = model or get_model()
    if active_model is None:
        return score_features_fallback(features)
    feature_array = np.asarray(features, dtype=float).reshape(1, -1)
    predicted_class = int(active_model.predict(feature_array)[0])
    confidence = float(active_model.predict_proba(feature_array).max())
    return PredictionResult(
        predicted_class=predicted_class,
        confidence=confidence,
    )


@app.middleware("http")
async def track_request_metrics(request: Request, call_next: object) -> Response:
    """Middleware para rastrear métricas de requisição.

    Args:
        request: Requisição HTTP.
        call_next: Próximo handler na cadeia.

    Returns:
        Resposta HTTP com métricas registradas.
    """
    path = request.url.path
    ACTIVE_REQUESTS.labels(endpoint=path).inc()
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start
    PREDICTION_LATENCY.labels(endpoint=path).observe(duration)
    ACTIVE_REQUESTS.labels(endpoint=path).dec()
    return response


@app.get("/metrics")
def metrics() -> Response:
    """Endpoint Prometheus para coleta de métricas.

    Returns:
        Métricas em formato Prometheus text.
    """
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )


@app.post("/predict")
def predict(request: PredictRequest) -> dict:
    """Endpoint de predição com métricas Prometheus.

    Args:
        request: Features de entrada.

    Returns:
        Predição com classe e confiança.
    """
    result = score_features(request.features)

    PREDICTION_COUNTER.labels(
        endpoint="/predict",
        predicted_class=str(result.predicted_class),
        status="success",
    ).inc()
    MODEL_CONFIDENCE.observe(result.confidence)

    return asdict(result)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check.

    Returns:
        Status da API.
    """
    return {"status": "ok"}
