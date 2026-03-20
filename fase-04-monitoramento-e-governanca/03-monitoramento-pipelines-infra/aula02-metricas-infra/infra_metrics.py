from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ResourceSample:
    timestamp: str
    cpu_percent: float
    memory_percent: float
    latency_ms: float
    gpu_percent: float = 0.0


def generate_resource_timeline() -> list[ResourceSample]:
    # Strategy-like contract: o coletor pode variar, mas a aula usa um sampler local fixo.
    return [
        ResourceSample("09:00", cpu_percent=48.0, memory_percent=58.0, latency_ms=120.0),
        ResourceSample("09:05", cpu_percent=67.0, memory_percent=71.0, latency_ms=158.0),
        ResourceSample("09:10", cpu_percent=91.0, memory_percent=84.0, latency_ms=246.0),
        ResourceSample("09:15", cpu_percent=88.0, memory_percent=87.0, latency_ms=232.0),
    ]


def compute_capacity_summary(samples: list[ResourceSample]) -> dict[str, float]:
    return {
        "peak_cpu_percent": max(sample.cpu_percent for sample in samples),
        "peak_memory_percent": max(sample.memory_percent for sample in samples),
        "peak_latency_ms": max(sample.latency_ms for sample in samples),
        "avg_latency_ms": round(sum(sample.latency_ms for sample in samples) / len(samples), 1),
    }


def detect_bottlenecks(samples: list[ResourceSample]) -> list[str]:
    bottlenecks: list[str] = []
    if any(sample.cpu_percent >= 90.0 for sample in samples):
        bottlenecks.append("cpu_saturation")
    if any(sample.memory_percent >= 85.0 for sample in samples):
        bottlenecks.append("memory_pressure")
    if any(sample.latency_ms >= 220.0 for sample in samples):
        bottlenecks.append("latency_spike")
    return bottlenecks


def run_infra_monitoring_demo() -> dict[str, object]:
    samples = generate_resource_timeline()
    return {
        "samples": [asdict(sample) for sample in samples],
        "summary": compute_capacity_summary(samples),
        "bottlenecks": detect_bottlenecks(samples),
    }


def main() -> None:
    results = run_infra_monitoring_demo()
    print("Metricas locais de infraestrutura\n")
    print(results["summary"])
    print(results["bottlenecks"])


if __name__ == "__main__":
    main()