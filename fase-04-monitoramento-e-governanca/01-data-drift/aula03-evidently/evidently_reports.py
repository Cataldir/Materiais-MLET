"""Relatorio local de drift com caminho opcional compativel com Evidently."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Protocol

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42
REFERENCE_ROWS = 600
CURRENT_ROWS = 240


@dataclass(frozen=True, slots=True)
class DriftBundle:
    """Conjunto de dados comparados pelo relatorio."""

    reference: pd.DataFrame
    current: pd.DataFrame


@dataclass(frozen=True, slots=True)
class FeatureDriftResult:
    """Resumo por feature para o relatorio."""

    feature: str
    drift_score: float
    mean_delta: float
    status: str


@dataclass(frozen=True, slots=True)
class MonitoringReport:
    """Saida serializavel do pack."""

    backend: str
    overall_status: str
    feature_results: tuple[FeatureDriftResult, ...]
    rendered_sections: tuple[str, ...]


class MonitoringAdapter(Protocol):
    """Contrato comum para backends de avaliacao."""

    backend_name: str

    def evaluate(self, bundle: DriftBundle) -> MonitoringReport:
        """Avalia drift entre referencia e lote atual."""


def _compute_ks_statistic(reference: np.ndarray, current: np.ndarray) -> float:
    reference_sorted = np.sort(reference.astype(float))
    current_sorted = np.sort(current.astype(float))
    combined = np.sort(np.concatenate([reference_sorted, current_sorted]))
    reference_cdf = np.searchsorted(reference_sorted, combined, side="right") / len(
        reference_sorted
    )
    current_cdf = np.searchsorted(current_sorted, combined, side="right") / len(
        current_sorted
    )
    return float(np.max(np.abs(reference_cdf - current_cdf)))


def _summarize_features(bundle: DriftBundle) -> tuple[FeatureDriftResult, ...]:
    feature_results: list[FeatureDriftResult] = []
    for column in bundle.reference.columns:
        drift_score = _compute_ks_statistic(
            bundle.reference[column].to_numpy(dtype=float),
            bundle.current[column].to_numpy(dtype=float),
        )
        mean_delta = float(bundle.current[column].mean() - bundle.reference[column].mean())
        if drift_score >= 0.18:
            status = "alert"
        elif drift_score >= 0.10:
            status = "watch"
        else:
            status = "ok"
        feature_results.append(
            FeatureDriftResult(
                feature=column,
                drift_score=drift_score,
                mean_delta=mean_delta,
                status=status,
            )
        )
    return tuple(feature_results)


class LocalStatisticsAdapter:
    """Adapter local que imita a estrutura de um relatorio de drift."""

    backend_name = "local"

    def evaluate(self, bundle: DriftBundle) -> MonitoringReport:
        feature_results = _summarize_features(bundle)
        overall_status = max(
            feature_results,
            key=lambda result: {"ok": 0, "watch": 1, "alert": 2}[result.status],
        ).status
        return MonitoringReport(
            backend=self.backend_name,
            overall_status=overall_status,
            feature_results=feature_results,
            rendered_sections=("summary", "data_drift", "drift_tests"),
        )


class EvidentlyAdapter(LocalStatisticsAdapter):
    """Adapter opcional ativado apenas quando a biblioteca existe."""

    backend_name = "evidently"

    def evaluate(self, bundle: DriftBundle) -> MonitoringReport:
        import evidently  # noqa: F401

        report = super().evaluate(bundle)
        return MonitoringReport(
            backend=self.backend_name,
            overall_status=report.overall_status,
            feature_results=report.feature_results,
            rendered_sections=("summary", "data_drift", "evidently_compatible_view"),
        )


class DriftReportTemplate(ABC):
    """Template Method para o fluxo didatico do relatorio."""

    def run(self) -> MonitoringReport:
        bundle = self.build_bundle()
        adapter = self.select_adapter()
        return adapter.evaluate(bundle)

    @abstractmethod
    def build_bundle(self) -> DriftBundle:
        """Cria os dados de referencia e lote atual."""

    @abstractmethod
    def select_adapter(self) -> MonitoringAdapter:
        """Seleciona o backend disponivel."""


class EvidentlyLessonPack(DriftReportTemplate):
    """Pack local-first para a aula de Evidently."""

    def __init__(self, random_state: int = RANDOM_STATE) -> None:
        self.random_state = random_state

    def build_bundle(self) -> DriftBundle:
        rng = np.random.default_rng(self.random_state)
        reference = pd.DataFrame(
            {
                "score_credito": rng.normal(640, 55, REFERENCE_ROWS).clip(300, 850),
                "tempo_cliente": rng.normal(24, 7, REFERENCE_ROWS).clip(1, 60),
                "gasto_mensal": rng.normal(180, 28, REFERENCE_ROWS).clip(40, 320),
            }
        )
        current = pd.DataFrame(
            {
                "score_credito": rng.normal(612, 62, CURRENT_ROWS).clip(300, 850),
                "tempo_cliente": rng.normal(28, 8, CURRENT_ROWS).clip(1, 60),
                "gasto_mensal": rng.normal(169, 33, CURRENT_ROWS).clip(40, 320),
            }
        )
        return DriftBundle(reference=reference, current=current)

    def select_adapter(self) -> MonitoringAdapter:
        try:
            import evidently  # noqa: F401
        except ImportError:
            return LocalStatisticsAdapter()
        return EvidentlyAdapter()


def run_evidently_lesson() -> MonitoringReport:
    """Executa o pack e devolve um relatorio serializavel."""

    return EvidentlyLessonPack().run()


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = run_evidently_lesson()
    LOGGER.info("backend=%s overall_status=%s", report.backend, report.overall_status)
    for result in report.feature_results:
        LOGGER.info(
            "%s | drift_score=%.3f | mean_delta=%.2f | status=%s",
            result.feature,
            result.drift_score,
            result.mean_delta,
            result.status,
        )


if __name__ == "__main__":
    main()