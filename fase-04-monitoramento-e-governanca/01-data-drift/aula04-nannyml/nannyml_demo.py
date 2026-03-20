"""Monitoramento sem labels com fallback local inspirado no NannyML."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 19


@dataclass(frozen=True, slots=True)
class NoLabelBatch:
    """Lote de inferencia com scores e classes previstas."""

    name: str
    probabilities: np.ndarray
    predictions: np.ndarray


@dataclass(frozen=True, slots=True)
class MonitoringEstimate:
    """Resultado de uma estrategia sem labels."""

    strategy: str
    estimated_quality: float
    alert: bool


@dataclass(frozen=True, slots=True)
class NoLabelReport:
    """Resumo consolidado da aula."""

    backend: str
    batch_name: str
    estimates: tuple[MonitoringEstimate, ...]
    average_quality: float


class EstimationStrategy(Protocol):
    """Contrato para estimadores sem labels."""

    name: str

    def estimate(self, reference: NoLabelBatch, current: NoLabelBatch) -> MonitoringEstimate:
        """Produz uma estimativa de qualidade para o lote atual."""


class ConfidenceProxyStrategy:
    """Usa queda de confianca media como proxy de degradacao."""

    name = "confidence_proxy"

    def estimate(self, reference: NoLabelBatch, current: NoLabelBatch) -> MonitoringEstimate:
        reference_confidence = np.maximum(reference.probabilities, 1 - reference.probabilities)
        current_confidence = np.maximum(current.probabilities, 1 - current.probabilities)
        drop = float(reference_confidence.mean() - current_confidence.mean())
        estimated_quality = float(np.clip(0.88 - drop * 2.2, 0.0, 1.0))
        return MonitoringEstimate(
            strategy=self.name,
            estimated_quality=estimated_quality,
            alert=estimated_quality < 0.72,
        )


class PredictionBalanceStrategy:
    """Mede mudanca na mistura de classes previstas."""

    name = "prediction_balance"

    def estimate(self, reference: NoLabelBatch, current: NoLabelBatch) -> MonitoringEstimate:
        reference_rate = float(reference.predictions.mean())
        current_rate = float(current.predictions.mean())
        delta = abs(current_rate - reference_rate)
        estimated_quality = float(np.clip(0.86 - delta * 1.8, 0.0, 1.0))
        return MonitoringEstimate(
            strategy=self.name,
            estimated_quality=estimated_quality,
            alert=delta >= 0.12,
        )


class LocalNoLabelAdapter:
    """Adapter local que agrega estrategias leves."""

    backend_name = "local"

    def __init__(self, strategies: tuple[EstimationStrategy, ...]) -> None:
        self.strategies = strategies

    def evaluate(self, reference: NoLabelBatch, current: NoLabelBatch) -> NoLabelReport:
        estimates = tuple(
            strategy.estimate(reference=reference, current=current)
            for strategy in self.strategies
        )
        average_quality = float(np.mean([estimate.estimated_quality for estimate in estimates]))
        return NoLabelReport(
            backend=self.backend_name,
            batch_name=current.name,
            estimates=estimates,
            average_quality=average_quality,
        )


class NannyMLAdapter(LocalNoLabelAdapter):
    """Adapter opcional ativado quando a biblioteca existe."""

    backend_name = "nannyml"

    def evaluate(self, reference: NoLabelBatch, current: NoLabelBatch) -> NoLabelReport:
        import nannyml  # noqa: F401

        return super().evaluate(reference=reference, current=current)


def build_batches(random_state: int = RANDOM_STATE) -> tuple[NoLabelBatch, NoLabelBatch]:
    """Gera lotes sinteticos de referencia e producao."""

    rng = np.random.default_rng(random_state)
    reference_probabilities = rng.beta(8, 3, size=500)
    reference_predictions = (reference_probabilities >= 0.5).astype(int)

    current_probabilities = rng.beta(5, 4, size=260)
    current_predictions = (current_probabilities >= 0.47).astype(int)

    return (
        NoLabelBatch(
            name="reference",
            probabilities=reference_probabilities,
            predictions=reference_predictions,
        ),
        NoLabelBatch(
            name="degraded_batch",
            probabilities=current_probabilities,
            predictions=current_predictions,
        ),
    )


def build_support_frame(report: NoLabelReport) -> pd.DataFrame:
    """Cria um DataFrame leve para exploracao local."""

    return pd.DataFrame(
        [
            {
                "strategy": estimate.strategy,
                "estimated_quality": estimate.estimated_quality,
                "alert": estimate.alert,
                "backend": report.backend,
                "batch_name": report.batch_name,
            }
            for estimate in report.estimates
        ]
    )


def run_nannyml_lesson() -> NoLabelReport:
    """Executa o pack com backend local ou opcional."""

    reference, current = build_batches()
    strategies: tuple[EstimationStrategy, ...] = (
        ConfidenceProxyStrategy(),
        PredictionBalanceStrategy(),
    )
    try:
        import nannyml  # noqa: F401
    except ImportError:
        adapter = LocalNoLabelAdapter(strategies)
    else:
        adapter = NannyMLAdapter(strategies)
    return adapter.evaluate(reference=reference, current=current)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = run_nannyml_lesson()
    frame = build_support_frame(report)
    LOGGER.info("backend=%s average_quality=%.3f", report.backend, report.average_quality)
    LOGGER.info("\n%s", frame.to_string(index=False))


if __name__ == "__main__":
    main()