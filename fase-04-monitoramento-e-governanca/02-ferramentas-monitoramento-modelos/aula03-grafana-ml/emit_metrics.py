"""Emissor deterministico de metricas para a stack local de Grafana."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 11


@dataclass(frozen=True, slots=True)
class MetricSample:
    """Representa uma metrica exposta no formato Prometheus."""

    name: str
    value: float
    labels: dict[str, str]


def build_metric_samples() -> tuple[MetricSample, ...]:
    """Gera um conjunto estavel de metricas de observabilidade."""

    return (
        MetricSample("ml_requests_total", 1280.0, {"model": "churn-v2", "route": "score"}),
        MetricSample("ml_prediction_latency_ms", 83.4, {"model": "churn-v2", "quantile": "p95"}),
        MetricSample("ml_prediction_error_rate", 0.012, {"model": "churn-v2"}),
        MetricSample("ml_drift_score", 0.17, {"model": "churn-v2", "feature": "gasto_mensal"}),
        MetricSample("ml_quality_gate_failures", 2.0, {"model": "churn-v2", "stage": "runtime"}),
    )


def render_prometheus_text(samples: tuple[MetricSample, ...] | None = None) -> str:
    """Converte as metricas em texto de exposition format."""

    active_samples = samples or build_metric_samples()
    lines: list[str] = []
    for sample in active_samples:
        if sample.labels:
            labels = ",".join(f'{key}="{value}"' for key, value in sample.labels.items())
            lines.append(f"{sample.name}{{{labels}}} {sample.value}")
        else:
            lines.append(f"{sample.name} {sample.value}")
    return "\n".join(lines) + "\n"


def export_metrics_snapshot(output_path: Path) -> Path:
    """Salva um snapshot local das metricas."""

    output_path.write_text(render_prometheus_text(), encoding="utf-8")
    return output_path


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    snapshot_path = export_metrics_snapshot(Path("metrics.prom"))
    LOGGER.info("snapshot salvo em %s", snapshot_path)
    LOGGER.info("\n%s", snapshot_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()