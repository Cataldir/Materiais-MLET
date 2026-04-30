"""Facade e Adapter para contratos de um microservico de inferencia."""

from __future__ import annotations

import logging
from dataclasses import asdict, dataclass

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)

REQUIRED_FIELDS = (
    "age",
    "income",
    "balance_ratio",
    "delinquency_count",
)


class SchemaValidationError(ValueError):
    """Erro de validacao de payload."""


@dataclass(frozen=True, slots=True)
class PredictionRequest:
    """Contrato interno de entrada para uma inferencia simples."""

    age: float
    income: float
    balance_ratio: float
    delinquency_count: int


@dataclass(frozen=True, slots=True)
class PredictionResponse:
    """Contrato padronizado de resposta do servico."""

    risk_score: float
    approved: bool
    model_version: str


def adapt_payload(payload: dict[str, object]) -> PredictionRequest:
    """Adapta um dict externo ao schema interno de request."""

    missing = [field_name for field_name in REQUIRED_FIELDS if field_name not in payload]
    if missing:
        raise SchemaValidationError(f"Campos obrigatorios ausentes: {missing}")

    request = PredictionRequest(
        age=float(payload["age"]),
        income=float(payload["income"]),
        balance_ratio=float(payload["balance_ratio"]),
        delinquency_count=int(payload["delinquency_count"]),
    )

    if request.age < 18:
        raise SchemaValidationError("idade minima de 18 anos")
    if request.income <= 0:
        raise SchemaValidationError("income deve ser positivo")
    if not 0 <= request.balance_ratio <= 1:
        raise SchemaValidationError("balance_ratio deve estar entre 0 e 1")
    if request.delinquency_count < 0:
        raise SchemaValidationError("delinquency_count nao pode ser negativo")
    return request


def score_request(request: PredictionRequest) -> float:
    """Calcula um score de risco deterministicamente."""

    score = 0.25
    score += min(request.balance_ratio * 0.35, 0.35)
    score += min(request.delinquency_count * 0.08, 0.24)
    score -= min(request.income / 200_000, 0.2)
    score -= min((request.age - 18) / 200, 0.1)
    return max(0.0, min(round(score, 4), 1.0))


@dataclass(frozen=True, slots=True)
class InferenceSchemaFacade:
    """Expõe health, readiness e predict sob um contrato unico."""

    model_version: str = "credit-risk-demo-1.0.0"

    def health(self) -> dict[str, str]:
        return {"status": "ok"}

    def ready(self) -> dict[str, str]:
        return {"status": "ready", "model_version": self.model_version}

    def predict(self, payload: dict[str, object]) -> PredictionResponse:
        request = adapt_payload(payload)
        risk_score = score_request(request)
        return PredictionResponse(
            risk_score=risk_score,
            approved=risk_score < 0.55,
            model_version=self.model_version,
        )


def main() -> None:
    """Executa um exemplo local de health, readiness e predict."""

    facade = InferenceSchemaFacade()
    payload = {
        "age": 37,
        "income": 82000,
        "balance_ratio": 0.28,
        "delinquency_count": 1,
    }
    LOGGER.info("health=%s", facade.health())
    LOGGER.info("ready=%s", facade.ready())
    LOGGER.info("predict=%s", asdict(facade.predict(payload)))


if __name__ == "__main__":
    main()