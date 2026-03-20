"""Uplift modeling local com estrategias leves e deterministicas."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

import numpy as np

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 34


@dataclass(frozen=True, slots=True)
class SegmentOutcome:
    """Resume o desempenho de um segmento sob tratamento e controle."""

    segment: str
    treated_rate: float
    control_rate: float
    uplift: float


@dataclass(frozen=True, slots=True)
class UpliftStrategyResult:
    """Resultado de uma estrategia de uplift."""

    strategy: str
    ranked_segments: tuple[SegmentOutcome, ...]


@dataclass(frozen=True, slots=True)
class UpliftDataset:
    """Dados sinteticos de tratamento e resposta."""

    segment_codes: np.ndarray
    treatment: np.ndarray
    outcome: np.ndarray
    segment_names: tuple[str, ...]


class UpliftStrategy(Protocol):
    """Contrato para estimadores de uplift."""

    name: str

    def estimate(self, dataset: UpliftDataset) -> UpliftStrategyResult:
        """Gera ranking de segmentos."""


def _aggregate_segment_uplift(dataset: UpliftDataset, adjustment: float = 0.0) -> tuple[SegmentOutcome, ...]:
    results: list[SegmentOutcome] = []
    for segment_index, segment_name in enumerate(dataset.segment_names):
        mask = dataset.segment_codes == segment_index
        treated = mask & (dataset.treatment == 1)
        control = mask & (dataset.treatment == 0)
        treated_rate = float(dataset.outcome[treated].mean())
        control_rate = float(dataset.outcome[control].mean())
        uplift = treated_rate - control_rate - adjustment
        results.append(
            SegmentOutcome(
                segment=segment_name,
                treated_rate=treated_rate,
                control_rate=control_rate,
                uplift=uplift,
            )
        )
    return tuple(sorted(results, key=lambda item: item.uplift, reverse=True))


class DifferenceInRatesStrategy:
    """Estimador direto por diferenca de taxas."""

    name = "difference_in_rates"

    def estimate(self, dataset: UpliftDataset) -> UpliftStrategyResult:
        return UpliftStrategyResult(self.name, _aggregate_segment_uplift(dataset))


class ShrinkageUpliftStrategy:
    """Versao conservadora com shrinkage uniforme do uplift."""

    name = "shrinkage_uplift"

    def estimate(self, dataset: UpliftDataset) -> UpliftStrategyResult:
        return UpliftStrategyResult(self.name, _aggregate_segment_uplift(dataset, adjustment=0.01))


class UpliftLessonTemplate(ABC):
    """Template Method para a sequencia da aula."""

    def run(self) -> tuple[UpliftStrategyResult, ...]:
        dataset = self.build_dataset()
        return tuple(strategy.estimate(dataset) for strategy in self.strategies())

    @abstractmethod
    def build_dataset(self) -> UpliftDataset:
        """Cria o experimento sintetico."""

    @abstractmethod
    def strategies(self) -> tuple[UpliftStrategy, ...]:
        """Retorna as estrategias comparadas."""


class UpliftLessonPack(UpliftLessonTemplate):
    """Implementacao concreta da aula de uplift."""

    def __init__(self, random_state: int = RANDOM_STATE) -> None:
        self.random_state = random_state

    def build_dataset(self) -> UpliftDataset:
        rng = np.random.default_rng(self.random_state)
        segment_names = ("baixo_risco", "alto_potencial", "reativacao")
        segment_codes = rng.choice([0, 1, 2], size=2400, p=[0.45, 0.30, 0.25])
        treatment = rng.binomial(1, 0.5, size=2400)
        baseline = np.select(
            [segment_codes == 0, segment_codes == 1, segment_codes == 2],
            [0.10, 0.18, 0.08],
        )
        incremental = np.select(
            [segment_codes == 0, segment_codes == 1, segment_codes == 2],
            [0.02, 0.09, 0.05],
        )
        probability = np.clip(baseline + incremental * treatment, 0.01, 0.95)
        outcome = rng.binomial(1, probability)
        return UpliftDataset(
            segment_codes=segment_codes,
            treatment=treatment,
            outcome=outcome,
            segment_names=segment_names,
        )

    def strategies(self) -> tuple[UpliftStrategy, ...]:
        return (DifferenceInRatesStrategy(), ShrinkageUpliftStrategy())


def run_uplift_demo() -> tuple[UpliftStrategyResult, ...]:
    """Executa o pack local de uplift."""

    return UpliftLessonPack().run()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for strategy_result in run_uplift_demo():
        LOGGER.info("strategy=%s", strategy_result.strategy)
        for segment in strategy_result.ranked_segments:
            LOGGER.info(
                "  %s | treated=%.3f control=%.3f uplift=%.3f",
                segment.segment,
                segment.treated_rate,
                segment.control_rate,
                segment.uplift,
            )


if __name__ == "__main__":
    main()