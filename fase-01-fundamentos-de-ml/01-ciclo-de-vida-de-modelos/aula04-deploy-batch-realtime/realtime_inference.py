"""Real-time inference — servidor FastAPI para inferência em tempo real.

Demonstra como servir um modelo treinado via API REST com
validação de entrada, health checks e logging de métricas.

Uso:
    uvicorn realtime_inference:app --host 0.0.0.0 --port 8000
"""

import logging
import pickle
import time
from pathlib import Path

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MODEL_PATH = Path("models/model.pkl")

app = FastAPI(
    title="ML Model API",
    description="API de inferência em tempo real para modelos sklearn",
    version="1.0.0",
)

_model: object | None = None


def get_model() -> object:
    """Carrega ou retorna o modelo em cache.

    Returns:
        Modelo carregado.

    Raises:
        RuntimeError: Se o modelo não estiver disponível.
    """
    global _model
    if _model is None:
        if not MODEL_PATH.exists():
            raise RuntimeError(f"Modelo não encontrado: {MODEL_PATH}")
        with open(MODEL_PATH, "rb") as f:
            _model = pickle.load(f)  # noqa: S301
        logger.info("Modelo carregado: %s", MODEL_PATH)
    return _model


class PredictRequest(BaseModel):
    """Schema de entrada para predição.

    Attributes:
        features: Lista de valores numéricos para predição.
    """

    features: list[float] = Field(..., min_length=1, description="Features numéricas")


class PredictResponse(BaseModel):
    """Schema de saída para predição.

    Attributes:
        prediction: Valor ou classe predita.
        probability: Probabilidade da predição (se disponível).
        latency_ms: Tempo de inferência em milissegundos.
    """

    prediction: float
    probability: float | None = None
    latency_ms: float


@app.get("/health")
def health_check() -> dict[str, str]:
    """Verifica se a API está respondendo.

    Returns:
        Status da API.
    """
    return {"status": "ok"}


@app.get("/ready")
def readiness_check() -> dict[str, str]:
    """Verifica se o modelo está carregado e pronto para predições.

    Returns:
        Status de prontidão.
    """
    try:
        get_model()
        return {"status": "ready"}
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest) -> PredictResponse:
    """Executa predição em tempo real.

    Args:
        request: Dados de entrada para predição.

    Returns:
        Predição com latência.
    """
    model = get_model()
    start = time.perf_counter()
    X = np.array(request.features).reshape(1, -1)

    prediction = float(model.predict(X)[0])
    probability = None
    if hasattr(model, "predict_proba"):
        probability = float(model.predict_proba(X).max())

    latency_ms = (time.perf_counter() - start) * 1000
    logger.info("Predição: %.4f | Latência: %.2fms", prediction, latency_ms)

    return PredictResponse(
        prediction=prediction,
        probability=probability,
        latency_ms=latency_ms,
    )
