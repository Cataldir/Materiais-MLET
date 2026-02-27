"""FastAPI instrumentada com Prometheus — métricas de latência e predições.

Demonstra como adicionar observabilidade a uma API de ML usando
prometheus-client para métricas de negócio e sistema.

Uso:
    uvicorn api_instrumented:app --host 0.0.0.0 --port 8000
    # Métricas disponíveis em http://localhost:8000/metrics
"""

import logging
import time

import numpy as np
from fastapi import FastAPI, Request, Response
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)
from pydantic import BaseModel
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PREDICTION_COUNTER = Counter(
    "ml_predictions_total",
    "Total de predições realizadas",
    ["endpoint", "predicted_class", "status"],
)
PREDICTION_LATENCY = Histogram(
    "ml_prediction_latency_seconds",
    "Latência das predições em segundos",
    ["endpoint"],
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)
MODEL_CONFIDENCE = Histogram(
    "ml_prediction_confidence",
    "Distribuição de confiança das predições",
    buckets=[0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 1.0],
)
ACTIVE_REQUESTS = Gauge(
    "ml_active_requests",
    "Número de requisições ativas",
    ["endpoint"],
)

app = FastAPI(title="ML API com Prometheus", version="1.0.0")

_model: RandomForestClassifier | None = None


def get_model() -> RandomForestClassifier:
    """Carrega ou retorna modelo em cache.

    Returns:
        Modelo treinado.
    """
    global _model
    if _model is None:
        X, y = load_iris(return_X_y=True)
        _model = RandomForestClassifier(n_estimators=50, random_state=42)
        _model.fit(X, y)
    return _model


class PredictRequest(BaseModel):
    """Schema de entrada para predição."""

    features: list[float]


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
    model = get_model()
    X = np.array(request.features).reshape(1, -1)
    predicted_class = int(model.predict(X)[0])
    confidence = float(model.predict_proba(X).max())

    PREDICTION_COUNTER.labels(
        endpoint="/predict",
        predicted_class=str(predicted_class),
        status="success",
    ).inc()
    MODEL_CONFIDENCE.observe(confidence)

    return {
        "predicted_class": predicted_class,
        "confidence": confidence,
    }


@app.get("/health")
def health() -> dict[str, str]:
    """Health check.

    Returns:
        Status da API.
    """
    return {"status": "ok"}
