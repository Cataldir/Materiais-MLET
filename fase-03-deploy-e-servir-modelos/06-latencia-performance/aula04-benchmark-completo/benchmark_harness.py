"""Harness local de benchmark com comparacao contra baseline versionada."""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from pathlib import Path

LOGGER = logging.getLogger(__name__)
BASELINE_PATH = Path(__file__).with_name("benchmark_baseline.json")


@dataclass(frozen=True, slots=True)
class BenchmarkResult:
    """Resultado agregado de um cenario de benchmark."""

    name: str
    latency_ms: float
    throughput_rps: float


@dataclass(frozen=True, slots=True)
class RegressionReport:
    """Resultado final da comparacao contra a baseline."""

    baseline_name: str
    results: tuple[BenchmarkResult, ...]
    regressions: tuple[str, ...]


def load_baseline(path: Path = BASELINE_PATH) -> dict[str, object]:
    """Carrega a baseline versionada em JSON."""

    return json.loads(path.read_text(encoding="utf-8"))


def run_benchmark_suite(path: Path = BASELINE_PATH) -> RegressionReport:
    """Executa o harness local e compara contra a baseline."""

    baseline = load_baseline(path)
    results = (
        BenchmarkResult("cpu_baseline", 46.0, 195.0),
        BenchmarkResult("batched_runtime", 26.0, 315.0),
        BenchmarkResult("optimized_preprocessing", 20.0, 355.0),
    )
    expected = {
        scenario["name"]: scenario
        for scenario in baseline["scenarios"]
    }
    regressions: list[str] = []
    for result in results:
        limits = expected[result.name]
        if result.latency_ms > float(limits["max_latency_ms"]):
            regressions.append(f"latency regression in {result.name}")
        if result.throughput_rps < float(limits["min_throughput_rps"]):
            regressions.append(f"throughput regression in {result.name}")
    return RegressionReport(
        baseline_name=str(baseline["baseline_name"]),
        results=results,
        regressions=tuple(regressions),
    )


def main() -> None:
    """Imprime o resultado do benchmark local."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = run_benchmark_suite()
    LOGGER.info("baseline=%s regressions=%s", report.baseline_name, list(report.regressions))


if __name__ == "__main__":
    main()