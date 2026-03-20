"""Pipeline local de drift com alertas por limiar para uso didatico.

Executa um fluxo deterministico de monitoramento sobre janelas sinteticas
de producao e classifica cada lote como ok, warn ou alert.

Uso:
    python drift_pipeline.py
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
REFERENCE_ROWS = 800
BATCH_ROWS = 240
DEFAULT_THRESHOLDS = None


@dataclass(frozen=True, slots=True)
class DriftThresholds:
    """Thresholds locais para classificacao de drift."""

    ks_warn: float = 0.10
    ks_alert: float = 0.18
    mean_shift_warn: float = 3.0
    mean_shift_alert: float = 8.0


@dataclass(frozen=True, slots=True)
class BatchWindow:
    """Representa um lote de producao avaliado pelo pipeline."""

    name: str
    data: pd.DataFrame


@dataclass(frozen=True, slots=True)
class FeatureAlert:
    """Resume o comportamento de uma feature em uma janela."""

    feature: str
    ks_statistic: float
    mean_shift: float
    status: str


@dataclass(frozen=True, slots=True)
class PipelineAlertSnapshot:
    """Resultado consolidado de uma janela monitorada."""

    batch_name: str
    overall_status: str
    drift_ratio: float
    triggered_features: list[str]
    feature_alerts: list[FeatureAlert]


def build_reference_frame(random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """Cria a base de referencia do monitoramento."""
    rng = np.random.default_rng(random_state)
    return pd.DataFrame(
        {
            "age": rng.normal(36, 8, REFERENCE_ROWS).clip(18, 75),
            "tenure_months": rng.normal(24, 6, REFERENCE_ROWS).clip(1, 48),
            "monthly_spend": rng.normal(180, 35, REFERENCE_ROWS).clip(50, 350),
        }
    )


def build_production_windows(random_state: int = RANDOM_STATE) -> list[BatchWindow]:
    """Gera janelas sinteticas com estabilidade e drift progressivo."""
    rng = np.random.default_rng(random_state + 1)
    windows = [
        BatchWindow(
            name="stable_batch",
            data=pd.DataFrame(
                {
                    "age": rng.normal(36.5, 8, BATCH_ROWS).clip(18, 75),
                    "tenure_months": rng.normal(24.5, 6, BATCH_ROWS).clip(1, 48),
                    "monthly_spend": rng.normal(181, 35, BATCH_ROWS).clip(50, 350),
                }
            ),
        ),
        BatchWindow(
            name="watch_batch",
            data=pd.DataFrame(
                {
                    "age": rng.normal(40, 9, BATCH_ROWS).clip(18, 75),
                    "tenure_months": rng.normal(27, 7, BATCH_ROWS).clip(1, 48),
                    "monthly_spend": rng.normal(171, 38, BATCH_ROWS).clip(50, 350),
                }
            ),
        ),
        BatchWindow(
            name="critical_batch",
            data=pd.DataFrame(
                {
                    "age": rng.normal(47, 10, BATCH_ROWS).clip(18, 75),
                    "tenure_months": rng.normal(31, 7, BATCH_ROWS).clip(1, 48),
                    "monthly_spend": rng.normal(156, 42, BATCH_ROWS).clip(50, 350),
                }
            ),
        ),
    ]
    return windows


def compute_ks_statistic(reference: np.ndarray, production: np.ndarray) -> float:
    """Calcula uma estatistica KS leve sem dependencias extras."""
    reference_sorted = np.sort(reference.astype(float))
    production_sorted = np.sort(production.astype(float))
    combined = np.sort(np.concatenate([reference_sorted, production_sorted]))
    reference_cdf = np.searchsorted(reference_sorted, combined, side="right") / len(
        reference_sorted
    )
    production_cdf = np.searchsorted(production_sorted, combined, side="right") / len(
        production_sorted
    )
    return float(np.max(np.abs(reference_cdf - production_cdf)))


def classify_feature_alert(
    reference: pd.Series,
    production: pd.Series,
    thresholds: DriftThresholds,
) -> FeatureAlert:
    """Classifica uma feature usando KS e deslocamento medio."""
    ks_statistic = compute_ks_statistic(
        reference.to_numpy(dtype=float),
        production.to_numpy(dtype=float),
    )
    mean_shift = float(production.mean() - reference.mean())
    absolute_shift = abs(mean_shift)

    if (
        ks_statistic >= thresholds.ks_alert
        or absolute_shift >= thresholds.mean_shift_alert
    ):
        status = "alert"
    elif (
        ks_statistic >= thresholds.ks_warn
        or absolute_shift >= thresholds.mean_shift_warn
    ):
        status = "warn"
    else:
        status = "ok"

    return FeatureAlert(
        feature=reference.name,
        ks_statistic=ks_statistic,
        mean_shift=mean_shift,
        status=status,
    )


def evaluate_batch(
    reference_frame: pd.DataFrame,
    batch: BatchWindow,
    thresholds: DriftThresholds,
) -> PipelineAlertSnapshot:
    """Avalia uma janela de producao contra a referencia."""
    feature_alerts = [
        classify_feature_alert(reference_frame[column], batch.data[column], thresholds)
        for column in reference_frame.columns
    ]
    status_priority = {"ok": 0, "warn": 1, "alert": 2}
    overall_status = max(
        feature_alerts, key=lambda alert: status_priority[alert.status]
    ).status
    triggered_features = [
        alert.feature for alert in feature_alerts if alert.status != "ok"
    ]
    drift_ratio = float(len(triggered_features) / len(feature_alerts))
    return PipelineAlertSnapshot(
        batch_name=batch.name,
        overall_status=overall_status,
        drift_ratio=drift_ratio,
        triggered_features=triggered_features,
        feature_alerts=feature_alerts,
    )


def run_monitoring_pipeline(
    random_state: int = RANDOM_STATE,
    thresholds: DriftThresholds | None = DEFAULT_THRESHOLDS,
) -> list[PipelineAlertSnapshot]:
    """Executa o fluxo fixo de monitoramento local da aula."""
    # Template Method via sequencia fixa: referencia -> janelas -> avaliacao -> resumo.
    active_thresholds = thresholds or DriftThresholds()
    reference_frame = build_reference_frame(random_state=random_state)
    windows = build_production_windows(random_state=random_state)
    snapshots = [
        evaluate_batch(
            reference_frame=reference_frame,
            batch=window,
            thresholds=active_thresholds,
        )
        for window in windows
    ]
    for snapshot in snapshots:
        logger.info(
            "%s | status=%s | drift_ratio=%.2f | triggered=%s",
            snapshot.batch_name,
            snapshot.overall_status,
            snapshot.drift_ratio,
            snapshot.triggered_features,
        )
    return snapshots


if __name__ == "__main__":
    run_monitoring_pipeline()
