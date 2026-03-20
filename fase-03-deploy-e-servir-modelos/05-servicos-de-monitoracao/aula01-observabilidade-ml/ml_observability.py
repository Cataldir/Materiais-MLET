"""Facade local para logs, metricas e traces em workloads de ML."""

from __future__ import annotations

import logging
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class LogEntry:
    """Representa uma linha de log de negocio."""

    message: str


@dataclass(frozen=True, slots=True)
class MetricPoint:
    """Representa uma metrica pontual de negocio."""

    name: str
    value: float


@dataclass(frozen=True, slots=True)
class TraceSpan:
    """Representa um span simples do fluxo de inferencia."""

    name: str
    duration_ms: float


@dataclass(frozen=True, slots=True)
class ObservabilitySummary:
    """Resumo do material capturado pelo facade."""

    logs: tuple[LogEntry, ...]
    metrics: tuple[MetricPoint, ...]
    traces: tuple[TraceSpan, ...]


class ObservabilityFacade:
    """Facade que encapsula os tres tipos de sinal observavel."""

    def __init__(self) -> None:
        self._logs: list[LogEntry] = []
        self._metrics: list[MetricPoint] = []
        self._traces: list[TraceSpan] = []

    def capture_prediction(
        self,
        request_id: str,
        latency_ms: float,
        predicted_class: int,
    ) -> ObservabilitySummary:
        self._logs.append(LogEntry(f"request={request_id} class={predicted_class}"))
        self._metrics.append(MetricPoint("prediction_latency_ms", latency_ms))
        self._traces.append(TraceSpan("predict", latency_ms))
        return ObservabilitySummary(
            logs=tuple(self._logs),
            metrics=tuple(self._metrics),
            traces=tuple(self._traces),
        )


def run_observability_demo() -> ObservabilitySummary:
    """Executa uma captura local de observabilidade."""

    facade = ObservabilityFacade()
    facade.capture_prediction("req-1", 42.0, 1)
    return facade.capture_prediction("req-2", 55.0, 0)


def main() -> None:
    """Mostra um resumo rapido do facade."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_observability_demo()
    LOGGER.info(
        "logs=%s metrics=%s traces=%s",
        len(summary.logs),
        len(summary.metrics),
        len(summary.traces),
    )


if __name__ == "__main__":
    main()