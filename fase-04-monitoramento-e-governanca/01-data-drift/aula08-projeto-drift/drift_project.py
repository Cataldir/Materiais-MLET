"""Projeto integrador local para monitoramento de drift."""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 53


@dataclass(frozen=True, slots=True)
class WindowSummary:
    """Resumo de uma janela operacional."""

    batch_name: str
    severity: str
    shifted_features: tuple[str, ...]
    recommended_action: str


@dataclass(frozen=True, slots=True)
class DriftProjectSummary:
    """Resumo consolidado do projeto."""

    windows: tuple[WindowSummary, ...]
    backlog_priority: tuple[str, ...]
    governance_note: str


def build_reference_frame(random_state: int = RANDOM_STATE) -> pd.DataFrame:
    """Cria a referencia local do projeto."""

    rng = np.random.default_rng(random_state)
    return pd.DataFrame(
        {
            "idade": rng.normal(36, 8, size=720).clip(18, 75),
            "renda": rng.normal(6500, 1200, size=720).clip(1800, 14000),
            "engajamento": rng.beta(3.5, 2.2, size=720),
        }
    )


def build_monitored_windows(random_state: int = RANDOM_STATE) -> dict[str, pd.DataFrame]:
    """Gera janelas sinteticas em progressao operacional."""

    rng = np.random.default_rng(random_state + 1)
    return {
        "baseline_window": pd.DataFrame(
            {
                "idade": rng.normal(36.5, 8, size=180).clip(18, 75),
                "renda": rng.normal(6400, 1250, size=180).clip(1800, 14000),
                "engajamento": rng.beta(3.4, 2.3, size=180),
            }
        ),
        "watch_window": pd.DataFrame(
            {
                "idade": rng.normal(41, 8.5, size=180).clip(18, 75),
                "renda": rng.normal(5900, 1350, size=180).clip(1800, 14000),
                "engajamento": rng.beta(3.0, 2.8, size=180),
            }
        ),
        "critical_window": pd.DataFrame(
            {
                "idade": rng.normal(47, 9.5, size=180).clip(18, 75),
                "renda": rng.normal(5200, 1500, size=180).clip(1800, 14000),
                "engajamento": rng.beta(2.4, 3.2, size=180),
            }
        ),
    }


def _mean_shift(reference: pd.Series, current: pd.Series) -> float:
    return float(current.mean() - reference.mean())


def _classify_severity(reference: pd.DataFrame, current: pd.DataFrame) -> WindowSummary:
    thresholds = {"idade": 3.0, "renda": 500.0, "engajamento": 0.08}
    shifts = {
        column: abs(_mean_shift(reference[column], current[column]))
        for column in reference.columns
    }
    shifted_features = tuple(
        column for column, value in shifts.items() if value >= thresholds[column]
    )
    pressure_score = sum(shifts[column] / thresholds[column] for column in shifted_features)
    if pressure_score >= 7.0:
        severity = "alert"
        action = "abrir incidente e priorizar retraining orientado por causa"
    elif pressure_score >= 3.5:
        severity = "watch"
        action = "acompanhar proximo lote e revisar segmentacao afetada"
    else:
        severity = "ok"
        action = "seguir monitorando sem intervencao"
    return WindowSummary(
        batch_name="",
        severity=severity,
        shifted_features=shifted_features,
        recommended_action=action,
    )


def run_drift_project() -> DriftProjectSummary:
    """Executa o fluxo integrador da aula de projeto."""

    reference = build_reference_frame()
    windows = build_monitored_windows()
    summaries: list[WindowSummary] = []
    for batch_name, frame in windows.items():
        summary = _classify_severity(reference=reference, current=frame)
        summaries.append(
            WindowSummary(
                batch_name=batch_name,
                severity=summary.severity,
                shifted_features=summary.shifted_features,
                recommended_action=summary.recommended_action,
            )
        )
    severity_rank = {"alert": 0, "watch": 1, "ok": 2}
    backlog_priority = tuple(
        summary.batch_name
        for summary in sorted(
            summaries,
            key=lambda item: (severity_rank[item.severity], -len(item.shifted_features)),
        )
    )
    return DriftProjectSummary(
        windows=tuple(summaries),
        backlog_priority=backlog_priority,
        governance_note="registrar evidencia do lote critico antes de promover novo modelo",
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_drift_project()
    for window in summary.windows:
        LOGGER.info(
            "%s | severity=%s | shifted=%s | action=%s",
            window.batch_name,
            window.severity,
            list(window.shifted_features),
            window.recommended_action,
        )
    LOGGER.info("backlog_priority=%s", list(summary.backlog_priority))
    LOGGER.info(summary.governance_note)


if __name__ == "__main__":
    main()