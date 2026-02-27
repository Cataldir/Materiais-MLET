"""API completa de inferência — FastAPI com carregamento de modelo e /predict.

Demonstra uma API de produção com:
- Carregamento lazy do modelo
- Validação de entrada com Pydantic
- Health/readiness checks
- Testes com TestClient

Uso:
    uvicorn api:app --host 0.0.0.0 --port 8000
"""

import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, AsyncGenerator

import numpy as np
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MODEL_STATE: dict[str, Any] = {}
IRIS_FEATURE_NAMES = ["sepal_length", "sepal_width", "petal_length", "petal_width"]
IRIS_TARGET_NAMES = ["setosa", "versicolor", "virginica"]


def train_demo_model() -> RandomForestClassifier:
    """Treina modelo demo no dataset Iris.

    Returns:
        Modelo treinado.
    """
    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X, y)
    logger.info("Modelo demo treinado no Iris dataset")
    return model


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Gerencia ciclo de vida da aplicação: carrega modelo na inicialização.

    Args:
        app: Instância da aplicação FastAPI.
    """
    MODEL_STATE["model"] = train_demo_model()
    logger.info("API inicializada com modelo carregado")
    yield
    MODEL_STATE.clear()
    logger.info("API encerrada")


app = FastAPI(
    title="Iris Classifier API",
    description="API de inferência para classificação de flores Iris",
    version="1.0.0",
    lifespan=lifespan,
)


class IrisPredictRequest(BaseModel):
    """Schema de entrada para predição Iris.

    Attributes:
        sepal_length: Comprimento da sépala (cm).
        sepal_width: Largura da sépala (cm).
        petal_length: Comprimento da pétala (cm).
        petal_width: Largura da pétala (cm).
    """

    sepal_length: float = Field(..., gt=0, le=20, description="Comprimento da sépala (cm)")
    sepal_width: float = Field(..., gt=0, le=20, description="Largura da sépala (cm)")
    petal_length: float = Field(..., gt=0, le=20, description="Comprimento da pétala (cm)")
    petal_width: float = Field(..., gt=0, le=20, description="Largura da pétala (cm)")


class IrisPredictResponse(BaseModel):
    """Schema de resposta para predição Iris.

    Attributes:
        predicted_class: Classe predita (índice).
        predicted_label: Nome da classe predita.
        probabilities: Probabilidades por classe.
        latency_ms: Tempo de inferência em ms.
    """

    predicted_class: int
    predicted_label: str
    probabilities: dict[str, float]
    latency_ms: float


@app.get("/health")
def health_check() -> dict[str, str]:
    """Verifica se a API está ativa.

    Returns:
        Status da API.
    """
    return {"status": "ok"}


@app.get("/ready")
def readiness_check() -> dict[str, str]:
    """Verifica se o modelo está carregado e pronto.

    Returns:
        Status de prontidão.

    Raises:
        HTTPException: Se o modelo não estiver disponível.
    """
    if "model" not in MODEL_STATE:
        raise HTTPException(status_code=503, detail="Modelo não disponível")
    return {"status": "ready", "model": "RandomForestClassifier"}


@app.post("/predict", response_model=IrisPredictResponse)
def predict(request: IrisPredictRequest) -> IrisPredictResponse:
    """Classifica uma flor Iris baseado nas medidas das pétalas e sépalas.

    Args:
        request: Medidas da flor.

    Returns:
        Predição com probabilidades e latência.

    Raises:
        HTTPException: Se o modelo não estiver disponível.
    """
    if "model" not in MODEL_STATE:
        raise HTTPException(status_code=503, detail="Modelo não disponível")

    model: RandomForestClassifier = MODEL_STATE["model"]
    features = np.array([[
        request.sepal_length, request.sepal_width,
        request.petal_length, request.petal_width,
    ]])

    start = time.perf_counter()
    predicted_class = int(model.predict(features)[0])
    probas = model.predict_proba(features)[0]
    latency_ms = (time.perf_counter() - start) * 1000

    probabilities = {
        name: float(prob)
        for name, prob in zip(IRIS_TARGET_NAMES, probas)
    }
    label = IRIS_TARGET_NAMES[predicted_class]
    logger.info("Predição: %s (%.2fms)", label, latency_ms)

    return IrisPredictResponse(
        predicted_class=predicted_class,
        predicted_label=label,
        probabilities=probabilities,
        latency_ms=latency_ms,
    )
