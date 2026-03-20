"""Projeto local de monitoramento composto por metricas, alertas e cards."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from statistics import mean

LOGGER = logging.getLogger(__name__)


class OverallStatus(StrEnum):
    """Status geral do sistema monitorado."""

    OK = "ok"
    ALERT = "alert"


@dataclass(frozen=True, slots=True)
class MonitoringEvent:
    """Evento bruto usado pelo projeto de monitoramento."""

    latency_ms: float
    success: bool
    drift_score: float


@dataclass(frozen=True, slots=True)
class DashboardCard:
    """Card simples de resumo para consumo operacional."""

    title: str
    value: str


@dataclass(frozen=True, slots=True)
class ProjectReport:
    """Saida consolidada do projeto de monitoramento."""

    overall_status: OverallStatus
    alerts: tuple[str, ...]
    cards: tuple[DashboardCard, ...]


class MonitoringProjectFacade:
    """Facade que consolida calculo de metricas e regras locais."""

    def run(self, events: tuple[MonitoringEvent, ...]) -> ProjectReport:
        latencies = [event.latency_ms for event in events]
        error_rate = 1.0 - (sum(event.success for event in events) / len(events))
        mean_drift = mean(event.drift_score for event in events)
        alerts: list[str] = []
        if max(latencies) > 250.0:
            alerts.append("latencia em degradacao")
        if error_rate > 0.05:
            alerts.append("erro acima do limite")
        if mean_drift > 0.20:
            alerts.append("drift medio exige investigacao")
        cards = (
            DashboardCard("p95 latency", f"{sorted(latencies)[-1]:.0f}ms"),
            DashboardCard("error rate", f"{error_rate:.2%}"),
            DashboardCard("mean drift", f"{mean_drift:.2f}"),
        )
        return ProjectReport(
            overall_status=OverallStatus.ALERT if alerts else OverallStatus.OK,
            alerts=tuple(alerts),
            cards=cards,
        )


def run_monitoring_project() -> ProjectReport:
    """Executa o projeto local com eventos de exemplo."""

    events = (
        MonitoringEvent(190.0, True, 0.12),
        MonitoringEvent(280.0, False, 0.24),
        MonitoringEvent(230.0, True, 0.27),
    )
    return MonitoringProjectFacade().run(events)


def main() -> None:
    """Imprime o resumo consolidado do mini projeto."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = run_monitoring_project()
    LOGGER.info("status=%s alerts=%s", report.overall_status, list(report.alerts))


if __name__ == "__main__":
    main()