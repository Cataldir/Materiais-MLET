"""API enxuta para demonstrar productization de modelo sequencial.

Material derivado do app de productization da branch ``origin/deep-learning``.
Para manter a baseline pública executável, o modelo LSTM original foi trocado
por um preditor determinístico de média móvel.
"""

from __future__ import annotations

import sys
from pathlib import Path
from statistics import fmean

from fastapi import FastAPI
from pydantic import BaseModel, Field

CURRENT_DIR = Path(__file__).resolve().parent
if str(CURRENT_DIR) not in sys.path:
    sys.path.append(str(CURRENT_DIR))

from quality_monitor import RollingQualityMonitor  # noqa: E402

SERVICE_NAME = "sequence-productization-reference"
QUALITY_MONITOR = RollingQualityMonitor(min_samples=5, max_history=200, tolerance=0.01)

app = FastAPI(title=SERVICE_NAME, version="1.0.0")


class InferenceRequest(BaseModel):
    """Contrato de entrada para inferência sequencial."""

    series: list[float] = Field(min_length=3, description="Janela de observações históricas.")
    observed_value: float | None = Field(default=None, description="Valor real mais recente, se já conhecido.")


class QualityRequest(BaseModel):
    """Contrato para atualizar o quality gate manualmente."""

    observed: float
    candidate_prediction: float
    baseline_prediction: float


def moving_average_predict(series: list[float], window_size: int = 3) -> float:
    """Prediz o próximo valor pela média móvel da janela final."""
    window = series[-window_size:]
    return float(fmean(window))


@app.get("/")
def health() -> dict[str, str]:
    """Health check simples."""
    return {"service": SERVICE_NAME, "status": "ok"}


@app.get("/readyz")
def ready() -> dict[str, str]:
    """Readiness check da referência canônica."""
    return {"status": "ready"}


@app.post("/infer")
def infer(request: InferenceRequest) -> dict[str, float | int | str]:
    """Executa inferência e atualiza o monitor se houver rótulo observado."""
    candidate_prediction = moving_average_predict(request.series)
    baseline_prediction = float(request.series[-1])
    response: dict[str, float | int | str] = {
        "candidate_prediction": candidate_prediction,
        "baseline_prediction": baseline_prediction,
        "series_length": len(request.series),
    }

    if request.observed_value is not None:
        snapshot = QUALITY_MONITOR.update(
            observed=request.observed_value,
            candidate=candidate_prediction,
            baseline=baseline_prediction,
        )
        response.update(snapshot.to_dict())

    return response


@app.post("/evaluate_quality")
def evaluate_quality(request: QualityRequest) -> dict[str, float | int | str]:
    """Atualiza o quality gate com dados observados."""
    return QUALITY_MONITOR.update(
        observed=request.observed,
        candidate=request.candidate_prediction,
        baseline=request.baseline_prediction,
    ).to_dict()