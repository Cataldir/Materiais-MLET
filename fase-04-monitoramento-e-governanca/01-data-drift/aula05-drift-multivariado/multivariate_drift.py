"""Comparacao local de drift multivariado com estrategias leves."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

import numpy as np

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 31


@dataclass(frozen=True, slots=True)
class MultivariateDataset:
    """Representa uma matriz multivariada."""

    reference: np.ndarray
    current: np.ndarray
    feature_names: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class DriftAssessment:
    """Resultado de uma estrategia multivariada."""

    strategy: str
    score: float
    status: str
    explanation: str


class MultivariateStrategy(Protocol):
    """Contrato para estrategias de drift conjunto."""

    name: str

    def compare(self, dataset: MultivariateDataset) -> DriftAssessment:
        """Compara referencia e lote atual."""


def _status_from_score(score: float, watch_threshold: float, alert_threshold: float) -> str:
    if score >= alert_threshold:
        return "alert"
    if score >= watch_threshold:
        return "watch"
    return "ok"


class RbfMmdStrategy:
    """Aproximacao leve de Maximum Mean Discrepancy com kernel RBF."""

    name = "rbf_mmd"

    def __init__(self, gamma: float = 0.25) -> None:
        self.gamma = gamma

    def _kernel_mean(self, left: np.ndarray, right: np.ndarray) -> float:
        diff = left[:, None, :] - right[None, :, :]
        sq_distance = np.sum(diff * diff, axis=2)
        return float(np.exp(-self.gamma * sq_distance).mean())

    def compare(self, dataset: MultivariateDataset) -> DriftAssessment:
        xx = self._kernel_mean(dataset.reference, dataset.reference)
        yy = self._kernel_mean(dataset.current, dataset.current)
        xy = self._kernel_mean(dataset.reference, dataset.current)
        score = max(xx + yy - 2 * xy, 0.0)
        return DriftAssessment(
            strategy=self.name,
            score=score,
            status=_status_from_score(score, watch_threshold=0.02, alert_threshold=0.05),
            explanation="mudanca conjunta capturada pelo kernel RBF",
        )


class ReconstructionResidualStrategy:
    """Usa PCA local para comparar erro de reconstrucao."""

    name = "reconstruction_residual"

    def compare(self, dataset: MultivariateDataset) -> DriftAssessment:
        centered_reference = dataset.reference - dataset.reference.mean(axis=0, keepdims=True)
        centered_current = dataset.current - dataset.reference.mean(axis=0, keepdims=True)
        _, _, vt = np.linalg.svd(centered_reference, full_matrices=False)
        components = vt[:2]
        projected = centered_current @ components.T
        reconstructed = projected @ components
        residual = centered_current - reconstructed
        score = float(np.mean(np.sum(residual * residual, axis=1)))
        return DriftAssessment(
            strategy=self.name,
            score=score,
            status=_status_from_score(score, watch_threshold=0.18, alert_threshold=0.35),
            explanation="aumento do erro de reconstrucao no subespaco de referencia",
        )


class MultivariateDriftTemplate(ABC):
    """Template Method para a sequencia fixa da aula."""

    def run(self) -> tuple[DriftAssessment, ...]:
        dataset = self.build_dataset()
        results = tuple(strategy.compare(dataset) for strategy in self.strategies())
        return tuple(sorted(results, key=lambda item: item.score, reverse=True))

    @abstractmethod
    def build_dataset(self) -> MultivariateDataset:
        """Gera os dados sinteticos da comparacao."""

    @abstractmethod
    def strategies(self) -> tuple[MultivariateStrategy, ...]:
        """Retorna as estrategias avaliadas."""


class MultivariateDriftLesson(MultivariateDriftTemplate):
    """Implementacao concreta da aula de drift multivariado."""

    def __init__(self, random_state: int = RANDOM_STATE) -> None:
        self.random_state = random_state

    def build_dataset(self) -> MultivariateDataset:
        rng = np.random.default_rng(self.random_state)
        latent_reference = rng.normal(size=(480, 2))
        latent_current = rng.normal(loc=(0.35, -0.25), scale=(1.0, 1.2), size=(220, 2))
        loading_reference = np.array(
            [
                [1.0, 0.2, 0.6],
                [0.5, 1.1, -0.4],
            ]
        )
        loading_current = np.array(
            [
                [1.0, 0.55, 0.2],
                [0.8, 0.9, -0.1],
            ]
        )
        reference = latent_reference @ loading_reference + rng.normal(0, 0.12, size=(480, 3))
        current = latent_current @ loading_current + rng.normal(0, 0.16, size=(220, 3))
        return MultivariateDataset(
            reference=reference,
            current=current,
            feature_names=("x_receita", "x_engajamento", "x_risco"),
        )

    def strategies(self) -> tuple[MultivariateStrategy, ...]:
        return (RbfMmdStrategy(), ReconstructionResidualStrategy())


def run_multivariate_drift_demo() -> tuple[DriftAssessment, ...]:
    """Executa a comparacao das estrategias."""

    return MultivariateDriftLesson().run()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for result in run_multivariate_drift_demo():
        LOGGER.info(
            "%s | score=%.4f | status=%s | %s",
            result.strategy,
            result.score,
            result.status,
            result.explanation,
        )


if __name__ == "__main__":
    main()