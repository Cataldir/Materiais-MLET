"""Avaliacao deterministica de regras de alerta para ML em producao."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum
from typing import Protocol

LOGGER = logging.getLogger(__name__)


class Severity(StrEnum):
    """Niveis de severidade suportados."""

    WARNING = "warning"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class MetricSnapshot:
    """Snapshot agregado usado para avaliacao de alertas."""

    p95_latency_ms: float
    error_rate: float
    drift_score: float


@dataclass(frozen=True, slots=True)
class AlertDecision:
    """Resultado da avaliacao de uma regra."""

    rule_name: str
    severity: Severity
    message: str


class AlertRule(Protocol):
    """Contrato de avaliacao de um snapshot."""

    def evaluate(self, snapshot: MetricSnapshot) -> AlertDecision | None:
        """Retorna um alerta ou nenhum sinal."""


class LatencyRule:
    """Dispara warning quando a latencia foge do esperado."""

    def evaluate(self, snapshot: MetricSnapshot) -> AlertDecision | None:
        if snapshot.p95_latency_ms > 250.0:
            return AlertDecision(
                "latency_p95",
                Severity.WARNING,
                "latencia acima do alvo operacional",
            )
        return None


class ErrorRateRule:
    """Dispara critical quando a taxa de erro ultrapassa o limite."""

    def evaluate(self, snapshot: MetricSnapshot) -> AlertDecision | None:
        if snapshot.error_rate > 0.05:
            return AlertDecision(
                "error_rate",
                Severity.CRITICAL,
                "taxa de erro acima do limite de producao",
            )
        return None


class DriftRule:
    """Dispara warning quando o drift sugere revisao do modelo."""

    def evaluate(self, snapshot: MetricSnapshot) -> AlertDecision | None:
        if snapshot.drift_score >= 0.25:
            return AlertDecision(
                "drift_score",
                Severity.WARNING,
                "drift acima do nivel de observacao",
            )
        return None


def evaluate_snapshot(snapshot: MetricSnapshot) -> tuple[AlertDecision, ...]:
    """Aplica todas as regras locais ao snapshot informado."""

    rules: tuple[AlertRule, ...] = (LatencyRule(), ErrorRateRule(), DriftRule())
    alerts = [alert for rule in rules if (alert := rule.evaluate(snapshot)) is not None]
    return tuple(alerts)


def main() -> None:
    """Executa um exemplo simples de alerta."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    snapshot = MetricSnapshot(p95_latency_ms=320.0, error_rate=0.08, drift_score=0.31)
    for alert in evaluate_snapshot(snapshot):
        LOGGER.info("%s -> %s", alert.rule_name, alert.severity)


if __name__ == "__main__":
    main()