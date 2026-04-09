"""
API de inferência FastAPI com instrumentação completa Prometheus.

Expõe métricas RED (Rate, Errors, Duration) e métricas específicas
de ML (confiança, distribuição de classes, features de entrada).
"""

import logging
import time

import mlflow
import numpy as np
from fastapi import FastAPI, HTTPException
from prometheus_client import make_asgi_app
from pydantic import BaseModel, Field

from src.common.config import settings
from src.common.metrics import (
    ACTIVE_MODELS_COUNT,
    INFERENCE_REQUEST_COUNT,
    INFERENCE_REQUEST_LATENCY,
    INPUT_FEATURE_VALUE,
    MODEL_INFO,
    MODEL_VERSION_GAUGE,
    PREDICTION_CLASS_COUNT,
    PREDICTION_CONFIDENCE,
)
from src.inference_pipeline.model_loader import ModelManager
from src.training_pipeline.drift_detector import DriftDetector

logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ML Inference API — Observável",
    description="API de inferência com métricas Prometheus integradas",
    version="1.0.0",
)

# Mount Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# Global model manager and drift detector
model_manager = ModelManager()
drift_detector = DriftDetector()

IRIS_CLASSES = ["setosa", "versicolor", "virginica"]
IRIS_FEATURES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]


class PredictionRequest(BaseModel):
    """Requisição de predição com features numéricas."""

    features: list[float] = Field(
        ...,
        min_length=4,
        max_length=4,
        description="Features do Iris dataset: [sepal_length, sepal_width, petal_length, petal_width]",
        examples=[[5.1, 3.5, 1.4, 0.2]],
    )


class PredictionResponse(BaseModel):
    """Resposta de predição com classe e confiança."""

    predicted_class: str
    predicted_class_id: int
    confidence: float
    model_name: str
    model_version: str
    latency_ms: float


class BatchPredictionRequest(BaseModel):
    """Requisição de predição em lote."""

    instances: list[list[float]] = Field(
        ...,
        min_length=1,
        description="Lista de instâncias para predição",
    )


class HealthResponse(BaseModel):
    """Resposta de health check."""

    status: str
    model_loaded: bool
    model_name: str | None = None
    model_version: str | None = None


@app.on_event("startup")
async def startup():
    """Carrega modelo e inicializa drift detector no startup."""
    try:
        model_manager.load_model()
        drift_detector.load_reference()

        MODEL_INFO.info({
            "model_name": settings.MODEL_NAME,
            "model_version": model_manager.model_version or "unknown",
            "framework": "sklearn",
        })
        ACTIVE_MODELS_COUNT.set(1)
        logger.info("Serviço de inferência inicializado com sucesso")
    except Exception as e:
        logger.error("Falha ao carregar modelo no startup: %s", e)
        ACTIVE_MODELS_COUNT.set(0)


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check do serviço."""
    return HealthResponse(
        status="healthy" if model_manager.model is not None else "degraded",
        model_loaded=model_manager.model is not None,
        model_name=settings.MODEL_NAME,
        model_version=model_manager.model_version,
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(request: PredictionRequest):
    """
    Realiza predição individual com métricas completas.

    Emite métricas de:
    - Latência (histogram)
    - Contagem de requisições (counter com status)
    - Confiança da predição (histogram)
    - Classe predita (counter)
    - Distribuição de features (histogram)
    """
    if model_manager.model is None:
        INFERENCE_REQUEST_COUNT.labels(
            model_name=settings.MODEL_NAME,
            model_version="none",
            status="error",
        ).inc()
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    start_time = time.time()
    model_version = model_manager.model_version or "unknown"

    try:
        X = np.array([request.features])

        # Record input feature distributions
        for i, feature_name in enumerate(IRIS_FEATURES):
            INPUT_FEATURE_VALUE.labels(feature_name=feature_name).observe(request.features[i])

        # Predict
        prediction = model_manager.model.predict(X)[0]
        probabilities = model_manager.model.predict_proba(X)[0]
        confidence = float(probabilities.max())
        predicted_class = IRIS_CLASSES[prediction]

        latency = time.time() - start_time

        # Emit metrics
        INFERENCE_REQUEST_COUNT.labels(
            model_name=settings.MODEL_NAME,
            model_version=model_version,
            status="success",
        ).inc()
        INFERENCE_REQUEST_LATENCY.labels(
            model_name=settings.MODEL_NAME,
            model_version=model_version,
        ).observe(latency)
        PREDICTION_CONFIDENCE.labels(
            model_name=settings.MODEL_NAME,
            predicted_class=predicted_class,
        ).observe(confidence)
        PREDICTION_CLASS_COUNT.labels(
            model_name=settings.MODEL_NAME,
            predicted_class=predicted_class,
        ).inc()

        return PredictionResponse(
            predicted_class=predicted_class,
            predicted_class_id=int(prediction),
            confidence=confidence,
            model_name=settings.MODEL_NAME,
            model_version=model_version,
            latency_ms=round(latency * 1000, 2),
        )

    except Exception as e:
        INFERENCE_REQUEST_COUNT.labels(
            model_name=settings.MODEL_NAME,
            model_version=model_version,
            status="error",
        ).inc()
        logger.error("Erro na predição: %s", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/predict/batch")
async def predict_batch(request: BatchPredictionRequest):
    """Predição em lote com drift check."""
    if model_manager.model is None:
        raise HTTPException(status_code=503, detail="Modelo não carregado")

    X = np.array(request.instances)

    # Run drift detection on batch
    drift_results = drift_detector.check_drift(X)

    predictions = model_manager.model.predict(X)
    probabilities = model_manager.model.predict_proba(X)

    results = []
    for i, (pred, probs) in enumerate(zip(predictions, probabilities)):
        predicted_class = IRIS_CLASSES[pred]
        confidence = float(probs.max())

        PREDICTION_CLASS_COUNT.labels(
            model_name=settings.MODEL_NAME,
            predicted_class=predicted_class,
        ).inc()

        results.append({
            "predicted_class": predicted_class,
            "predicted_class_id": int(pred),
            "confidence": confidence,
        })

    return {
        "predictions": results,
        "drift_analysis": drift_results,
        "batch_size": len(request.instances),
    }


@app.post("/model/reload")
async def reload_model():
    """Recarrega o modelo do MLflow Registry."""
    try:
        model_manager.load_model()
        MODEL_INFO.info({
            "model_name": settings.MODEL_NAME,
            "model_version": model_manager.model_version or "unknown",
            "framework": "sklearn",
        })
        return {"status": "reloaded", "version": model_manager.model_version}
    except Exception as e:
        logger.error("Falha ao recarregar modelo: %s", e)
        raise HTTPException(status_code=500, detail=str(e))
