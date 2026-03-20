from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class MonitoringBatch:
    name: str
    latency_ms: float
    error_rate: float
    drift_score: float


def load_mlflow_module():
    try:
        import mlflow

        return mlflow
    except ImportError:
        return None


def build_monitoring_batches() -> list[MonitoringBatch]:
    return [
        MonitoringBatch("stable_batch", latency_ms=120.0, error_rate=0.01, drift_score=0.08),
        MonitoringBatch("watch_batch", latency_ms=165.0, error_rate=0.04, drift_score=0.21),
        MonitoringBatch("critical_batch", latency_ms=245.0, error_rate=0.09, drift_score=0.44),
    ]


def classify_batch(batch: MonitoringBatch) -> str:
    if batch.error_rate >= 0.08 or batch.drift_score >= 0.40:
        return "alert"
    if batch.error_rate >= 0.03 or batch.drift_score >= 0.20:
        return "watch"
    return "ok"


def track_batches(output_dir: Path | None = None) -> dict[str, object]:
    tracking_dir = output_dir or Path(__file__).parent / "tracking_artifacts"
    tracking_dir.mkdir(exist_ok=True)
    batches = build_monitoring_batches()
    mlflow = load_mlflow_module()

    # Observer-like flow: each batch emits metrics to a tracking sink.
    batch_summaries = [
        {
            **asdict(batch),
            "status": classify_batch(batch),
        }
        for batch in batches
    ]

    if mlflow is not None:
        mlflow.set_tracking_uri((tracking_dir / "mlruns").as_uri())
        with mlflow.start_run(run_name="mlflow-monitoramento-local"):
            for summary in batch_summaries:
                mlflow.log_metrics(
                    {
                        f"{summary['name']}_latency_ms": summary["latency_ms"],
                        f"{summary['name']}_error_rate": summary["error_rate"],
                        f"{summary['name']}_drift_score": summary["drift_score"],
                    }
                )
            mlflow.log_dict({"batches": batch_summaries}, "monitoring_summary.json")
    else:
        (tracking_dir / "monitoring_summary.json").write_text(
            json.dumps({"batches": batch_summaries}, indent=2),
            encoding="utf-8",
        )

    return {
        "mlflow_available": mlflow is not None,
        "batches": batch_summaries,
        "tracking_dir": str(tracking_dir),
    }


def main() -> None:
    results = track_batches()
    print("Monitoramento continuo com MLflow local\n")
    for batch in results["batches"]:
        print(
            f"- {batch['name']}: latency={batch['latency_ms']:.0f}ms, "
            f"error_rate={batch['error_rate']:.2f}, drift={batch['drift_score']:.2f} -> {batch['status']}"
        )
    print(f"\nMLflow disponivel: {results['mlflow_available']}")


if __name__ == "__main__":
    main()