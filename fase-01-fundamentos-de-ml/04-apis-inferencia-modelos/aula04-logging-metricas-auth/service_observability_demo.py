"""Decorators e Chain of Responsibility para um servico de inferencia local."""

from __future__ import annotations

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ServiceRequest:
    """Request simplificado para o fluxo de inferencia."""

    token: str
    payload: dict[str, float]


@dataclass(frozen=True, slots=True)
class ServiceResponse:
    """Resposta padronizada do servico."""

    status_code: int
    body: dict[str, object]


@dataclass(slots=True)
class ServiceRuntime:
    """Estado operacional necessario para auth e metricas."""

    valid_tokens: set[str] = field(default_factory=lambda: {"mlet-token"})
    quota_per_token: int = 2
    token_calls: dict[str, int] = field(default_factory=dict)
    total_calls: int = 0
    successful_calls: int = 0
    rejected_calls: int = 0
    latencies_ms: list[float] = field(default_factory=list)

    def metrics_snapshot(self) -> dict[str, float]:
        average_latency = 0.0
        if self.latencies_ms:
            average_latency = sum(self.latencies_ms) / len(self.latencies_ms)
        return {
            "total_calls": float(self.total_calls),
            "successful_calls": float(self.successful_calls),
            "rejected_calls": float(self.rejected_calls),
            "avg_latency_ms": round(average_latency, 4),
        }


class Handler:
    """Elemento base da cadeia de responsabilidades."""

    def __init__(self, next_handler: Handler | None = None):
        self.next_handler = next_handler

    def handle(self, request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        if self.next_handler is None:
            raise RuntimeError("cadeia incompleta")
        return self.next_handler.handle(request, runtime)


class AuthHandler(Handler):
    """Valida token antes da inferencia."""

    def handle(self, request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        runtime.total_calls += 1
        if request.token not in runtime.valid_tokens:
            runtime.rejected_calls += 1
            return ServiceResponse(401, {"error": "token invalido"})
        return super().handle(request, runtime)


class QuotaHandler(Handler):
    """Garante uma cota simples por token."""

    def handle(self, request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        current_calls = runtime.token_calls.get(request.token, 0)
        if current_calls >= runtime.quota_per_token:
            runtime.rejected_calls += 1
            return ServiceResponse(429, {"error": "quota excedida"})
        runtime.token_calls[request.token] = current_calls + 1
        return super().handle(request, runtime)


class PayloadHandler(Handler):
    """Valida o payload antes de chamar o handler final."""

    def handle(self, request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        for field_name in ("score_base", "volatility"):
            if field_name not in request.payload:
                runtime.rejected_calls += 1
                return ServiceResponse(422, {"error": f"campo ausente: {field_name}"})
        return super().handle(request, runtime)


def with_logging(handler: Callable[[ServiceRequest, ServiceRuntime], ServiceResponse]) -> Callable[[ServiceRequest, ServiceRuntime], ServiceResponse]:
    """Decorator que registra entrada e saida do handler."""

    def wrapped(request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        LOGGER.info("request token=%s payload=%s", request.token, request.payload)
        response = handler(request, runtime)
        LOGGER.info("response status=%s body=%s", response.status_code, response.body)
        return response

    return wrapped


def with_metrics(handler: Callable[[ServiceRequest, ServiceRuntime], ServiceResponse]) -> Callable[[ServiceRequest, ServiceRuntime], ServiceResponse]:
    """Decorator que mede latencia e atualiza metricas agregadas."""

    def wrapped(request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        start = time.perf_counter()
        response = handler(request, runtime)
        latency_ms = (time.perf_counter() - start) * 1000
        runtime.latencies_ms.append(latency_ms)
        if response.status_code < 400:
            runtime.successful_calls += 1
        return response

    return wrapped


@with_logging
@with_metrics
def predict_handler(request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
    """Handler principal com a regra de negocio da inferencia."""

    score = request.payload["score_base"] + request.payload["volatility"] * 0.3
    approved = score < 0.7
    return ServiceResponse(200, {"approved": approved, "score": round(score, 4)})


class TerminalHandler(Handler):
    """Fecha a cadeia e delega ao handler decorado."""

    def handle(self, request: ServiceRequest, runtime: ServiceRuntime) -> ServiceResponse:
        return predict_handler(request, runtime)


def build_chain() -> Handler:
    """Monta a ordem de auth, quota, payload e regra principal."""

    return AuthHandler(QuotaHandler(PayloadHandler(TerminalHandler())))


def process_service_call(
    runtime: ServiceRuntime,
    token: str,
    payload: dict[str, float],
) -> ServiceResponse:
    """Executa uma chamada no pipeline completo de observabilidade."""

    chain = build_chain()
    return chain.handle(ServiceRequest(token=token, payload=payload), runtime)


def main() -> None:
    """Executa uma chamada valida e mostra metricas agregadas."""

    runtime = ServiceRuntime()
    response = process_service_call(
        runtime,
        token="mlet-token",
        payload={"score_base": 0.31, "volatility": 0.22},
    )
    LOGGER.info("status=%s body=%s", response.status_code, response.body)
    LOGGER.info("metrics=%s", runtime.metrics_snapshot())


if __name__ == "__main__":
    main()