"""Colecao local de metricas de producao no estilo observer."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from math import ceil
from statistics import mean
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PredictionEvent:
    """Evento basico emitido por uma inferencia em producao."""

    latency_ms: float
    success: bool
    confidence: float


@dataclass(frozen=True, slots=True)
class ProductionWindow:
    """Resumo agregado da janela observada."""

    total_requests: int
    p95_latency_ms: float
    error_rate: float
    average_confidence: float


class EventObserver(Protocol):
    """Contrato dos coletores acoplados ao hub de telemetria."""

    def observe(self, event: PredictionEvent) -> None:
        """Recebe um evento individual para agregacao."""


class LatencyObserver:
    """Mantem o historico local de latencias."""

    def __init__(self) -> None:
        self.latencies: list[float] = []

    def observe(self, event: PredictionEvent) -> None:
        self.latencies.append(event.latency_ms)


class ErrorObserver:
    """Mantem o historico de sucessos e falhas."""

    def __init__(self) -> None:
        self.success_flags: list[bool] = []

    def observe(self, event: PredictionEvent) -> None:
        self.success_flags.append(event.success)


class ConfidenceObserver:
    """Mantem o historico de confianca de predito."""

    def __init__(self) -> None:
        self.confidences: list[float] = []

    def observe(self, event: PredictionEvent) -> None:
        self.confidences.append(event.confidence)


class TelemetryHub:
    """Hub local que distribui eventos para observadores."""

    def __init__(self, observers: tuple[EventObserver, ...]) -> None:
        self.observers = observers

    def publish(self, event: PredictionEvent) -> None:
        for observer in self.observers:
            observer.observe(event)


def simulate_metrics_window() -> ProductionWindow:
    """Simula uma pequena janela operacional com telemetria local."""

    latency_observer = LatencyObserver()
    error_observer = ErrorObserver()
    confidence_observer = ConfidenceObserver()
    hub = TelemetryHub((latency_observer, error_observer, confidence_observer))
    events = (
        PredictionEvent(82.0, True, 0.95),
        PredictionEvent(96.0, True, 0.91),
        PredictionEvent(110.0, False, 0.52),
        PredictionEvent(89.0, True, 0.88),
        PredictionEvent(140.0, True, 0.83),
    )
    for event in events:
        hub.publish(event)
    ordered_latencies = sorted(latency_observer.latencies)
    p95_index = max(0, ceil(len(ordered_latencies) * 0.95) - 1)
    return ProductionWindow(
        total_requests=len(events),
        p95_latency_ms=ordered_latencies[p95_index],
        error_rate=1.0 - (sum(error_observer.success_flags) / len(events)),
        average_confidence=float(mean(confidence_observer.confidences)),
    )


def main() -> None:
    """Exibe o resumo da janela observada."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    window = simulate_metrics_window()
    LOGGER.info(
        "requests=%s p95=%.1f error_rate=%.2f",
        window.total_requests,
        window.p95_latency_ms,
        window.error_rate,
    )


if __name__ == "__main__":
    main()