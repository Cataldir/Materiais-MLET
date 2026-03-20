"""Estimacao de efeito causal com dados sinteticos e ajustes leves.

Este pack evita bibliotecas causais pesadas para manter o material executavel em
qualquer ambiente local, mas preserva a logica pedagogica de comparar um efeito
ingenuo com estimativas ajustadas.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

import numpy as np

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 7
TRUE_ATE = 2.5


@dataclass(frozen=True)
class SyntheticCausalStudy:
    """Armazena os vetores principais do experimento sintetico."""

    engagement_score: np.ndarray
    loyalty_segment: np.ndarray
    treatment: np.ndarray
    outcome: np.ndarray
    true_ate: float


@dataclass(frozen=True)
class EstimationSummary:
    """Resumo serializavel de um estimador causal."""

    estimator: str
    estimated_ate: float
    bias: float


class CausalEstimator(Protocol):
    """Contrato comum para estrategias de estimacao."""

    name: str

    def estimate(self, study: SyntheticCausalStudy) -> float:
        """Estima o ATE a partir do estudo sintetico."""


class NaiveDifferenceInMeansEstimator:
    """Diferenca simples de medias sem ajuste por confundidores."""

    name = "naive_difference"

    def estimate(self, study: SyntheticCausalStudy) -> float:
        treated_mask = study.treatment == 1
        control_mask = ~treated_mask
        return float(
            study.outcome[treated_mask].mean() - study.outcome[control_mask].mean()
        )


class StratifiedDifferenceEstimator:
    """Ajusta o efeito por estratos do confundidor principal."""

    name = "stratified_difference"

    def __init__(self, bins: int = 5) -> None:
        self.bins = bins

    def estimate(self, study: SyntheticCausalStudy) -> float:
        quantiles = np.quantile(
            study.engagement_score, np.linspace(0.0, 1.0, self.bins + 1)
        )
        total_weight = 0.0
        weighted_effect = 0.0
        for left, right in zip(quantiles[:-1], quantiles[1:], strict=True):
            if right == quantiles[-1]:
                mask = (study.engagement_score >= left) & (
                    study.engagement_score <= right
                )
            else:
                mask = (study.engagement_score >= left) & (
                    study.engagement_score < right
                )
            treated = mask & (study.treatment == 1)
            control = mask & (study.treatment == 0)
            if treated.sum() == 0 or control.sum() == 0:
                continue
            local_effect = study.outcome[treated].mean() - study.outcome[control].mean()
            weight = float(mask.sum())
            weighted_effect += float(local_effect) * weight
            total_weight += weight
        if total_weight == 0.0:
            return 0.0
        return weighted_effect / total_weight


class RegressionAdjustmentEstimator:
    """Estima o efeito via regressao linear com covariaveis observadas."""

    name = "regression_adjustment"

    def estimate(self, study: SyntheticCausalStudy) -> float:
        design_matrix = np.column_stack(
            [
                np.ones_like(study.treatment, dtype=float),
                study.treatment.astype(float),
                study.engagement_score.astype(float),
                study.loyalty_segment.astype(float),
                (study.engagement_score * study.loyalty_segment).astype(float),
            ]
        )
        coefficients, *_ = np.linalg.lstsq(
            design_matrix, study.outcome.astype(float), rcond=None
        )
        return float(coefficients[1])


class CausalPackTemplate(ABC):
    """Template Method para manter o fluxo do experimento estavel."""

    def run(self) -> tuple[EstimationSummary, ...]:
        study = self.build_study()
        summaries = [self.evaluate(estimator, study) for estimator in self.estimators()]
        summaries.sort(key=lambda summary: abs(summary.bias))
        return tuple(summaries)

    @abstractmethod
    def build_study(self) -> SyntheticCausalStudy:
        """Cria um estudo sintetico reprodutivel."""

    @abstractmethod
    def estimators(self) -> tuple[CausalEstimator, ...]:
        """Retorna os estimadores comparados pelo pack."""

    def evaluate(
        self, estimator: CausalEstimator, study: SyntheticCausalStudy
    ) -> EstimationSummary:
        estimated_ate = estimator.estimate(study)
        return EstimationSummary(
            estimator=estimator.name,
            estimated_ate=estimated_ate,
            bias=estimated_ate - study.true_ate,
        )


class SyntheticCausalEffectPack(CausalPackTemplate):
    """Executa a comparacao entre estimadores leves de efeito causal."""

    def __init__(self, sample_size: int = 2_000, seed: int = RANDOM_STATE) -> None:
        self.sample_size = sample_size
        self.seed = seed

    def build_study(self) -> SyntheticCausalStudy:
        rng = np.random.default_rng(self.seed)
        engagement_score = rng.normal(loc=0.0, scale=1.0, size=self.sample_size)
        loyalty_segment = rng.integers(0, 2, size=self.sample_size)
        logits = -0.3 + 1.2 * engagement_score + 0.5 * loyalty_segment
        treatment_probability = 1.0 / (1.0 + np.exp(-logits))
        treatment = rng.binomial(1, treatment_probability)

        baseline = 6.0 + 1.7 * engagement_score + 0.9 * loyalty_segment
        noise = rng.normal(loc=0.0, scale=0.8, size=self.sample_size)
        outcome = baseline + TRUE_ATE * treatment + noise
        return SyntheticCausalStudy(
            engagement_score=engagement_score,
            loyalty_segment=loyalty_segment,
            treatment=treatment,
            outcome=outcome,
            true_ate=TRUE_ATE,
        )

    def estimators(self) -> tuple[CausalEstimator, ...]:
        return (
            NaiveDifferenceInMeansEstimator(),
            StratifiedDifferenceEstimator(),
            RegressionAdjustmentEstimator(),
        )


def run_causal_effect_demo() -> dict[str, EstimationSummary]:
    """Executa o pack e devolve resumos indexados por nome do estimador."""

    summaries = SyntheticCausalEffectPack().run()
    return {summary.estimator: summary for summary in summaries}


def main() -> None:
    """Executa a demonstracao local com logging."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summaries = run_causal_effect_demo()
    for name, summary in summaries.items():
        LOGGER.info(
            "%s -> estimated_ate=%.3f bias=%.3f",
            name,
            summary.estimated_ate,
            summary.bias,
        )
    LOGGER.info("true_ate=%.3f", TRUE_ATE)


if __name__ == "__main__":
    main()
