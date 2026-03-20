"""Monitoramento prescritivo local com fluxo observer-like."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class SegmentSignal:
    """Sinal observado para um segmento monitorado."""

    segment: str
    uplift: float
    risk_level: str
    capacity_available: bool


@dataclass(frozen=True, slots=True)
class Recommendation:
    """Recomendacao prescritiva gerada a partir do sinal."""

    segment: str
    action: str
    priority: str
    rationale: str


class RecommendationStrategy(Protocol):
    """Contrato para decidir a acao recomendada."""

    name: str

    def recommend(self, signal: SegmentSignal) -> Recommendation:
        """Produz a recomendacao para um segmento."""


class CapacityAwareStrategy:
    """Prioriza segmentos por uplift, risco e capacidade de execucao."""

    name = "capacity_aware"

    def recommend(self, signal: SegmentSignal) -> Recommendation:
        if signal.uplift >= 0.06 and signal.capacity_available:
            return Recommendation(
                segment=signal.segment,
                action="acionar campanha causal direcionada",
                priority="high",
                rationale="uplift alto com capacidade disponivel",
            )
        if signal.risk_level == "high":
            return Recommendation(
                segment=signal.segment,
                action="abrir analise de causa raiz antes de escalar incentivo",
                priority="high",
                rationale="risco alto exige revisao antes da intervencao",
            )
        return Recommendation(
            segment=signal.segment,
            action="manter observacao e coletar mais evidencia",
            priority="medium",
            rationale="efeito incremental moderado ou capacidade restrita",
        )


class RecommendationObserver(Protocol):
    """Contrato para consumidores da recomendacao."""

    name: str

    def notify(self, recommendation: Recommendation) -> str:
        """Transforma a recomendacao em uma mensagem local."""


class OperationsObserver:
    """Representa o time operacional."""

    name = "operations"

    def notify(self, recommendation: Recommendation) -> str:
        return f"operations::{recommendation.segment}::{recommendation.priority}::{recommendation.action}"


class GovernanceObserver:
    """Representa a camada de evidencia e governanca."""

    name = "governance"

    def notify(self, recommendation: Recommendation) -> str:
        return f"governance::{recommendation.segment}::{recommendation.rationale}"


def build_segment_signals() -> tuple[SegmentSignal, ...]:
    """Gera os sinais usados pela aula."""

    return (
        SegmentSignal("alto_potencial", uplift=0.08, risk_level="medium", capacity_available=True),
        SegmentSignal("reativacao", uplift=0.05, risk_level="high", capacity_available=True),
        SegmentSignal("baixo_risco", uplift=0.02, risk_level="low", capacity_available=False),
    )


def run_prescriptive_monitoring() -> dict[str, object]:
    """Executa o fluxo de recomendacao e distribuicao local."""

    strategy = CapacityAwareStrategy()
    observers: tuple[RecommendationObserver, ...] = (OperationsObserver(), GovernanceObserver())
    recommendations = tuple(strategy.recommend(signal) for signal in build_segment_signals())
    notifications = {
        observer.name: [observer.notify(recommendation) for recommendation in recommendations]
        for observer in observers
    }
    return {
        "strategy": strategy.name,
        "recommendations": recommendations,
        "notifications": notifications,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_prescriptive_monitoring()
    LOGGER.info("strategy=%s", summary["strategy"])
    for recommendation in summary["recommendations"]:
        LOGGER.info(
            "%s | priority=%s | action=%s | rationale=%s",
            recommendation.segment,
            recommendation.priority,
            recommendation.action,
            recommendation.rationale,
        )
    LOGGER.info("notifications=%s", summary["notifications"])


if __name__ == "__main__":
    main()