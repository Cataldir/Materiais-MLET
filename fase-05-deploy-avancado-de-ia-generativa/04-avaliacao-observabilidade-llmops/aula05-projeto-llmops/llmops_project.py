from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TraceRecord:
    """Trace sintetico para reexecucao local."""

    name: str
    total_tokens: int
    latency_ms: float
    grounded: bool


TRACE_DATA = [
    TraceRecord("stable_trace", total_tokens=280, latency_ms=82.0, grounded=True),
    TraceRecord("watch_trace", total_tokens=420, latency_ms=118.0, grounded=True),
    TraceRecord("failing_trace", total_tokens=560, latency_ms=148.0, grounded=False),
]


def enrich_trace(trace: TraceRecord) -> dict[str, object]:
    """Filtro 1: normaliza e adiciona custo estimado."""

    return {
        "name": trace.name,
        "total_tokens": trace.total_tokens,
        "latency_ms": trace.latency_ms,
        "grounded": trace.grounded,
        "estimated_cost_usd": round(trace.total_tokens * 0.000002, 6),
    }


def evaluate_trace(payload: dict[str, object]) -> dict[str, object]:
    """Filtro 2: calcula decisao deterministica."""

    decision = "pass"
    if payload["latency_ms"] >= 110.0 or payload["estimated_cost_usd"] >= 0.001:
        decision = "warn"
    if not payload["grounded"] or payload["latency_ms"] >= 140.0:
        decision = "fail"
    payload = dict(payload)
    payload["decision"] = decision
    return payload


def summarize_pipeline(records: list[dict[str, object]]) -> dict[str, object]:
    """Filtro 3: consolida o replay inteiro."""

    return {
        "records": records,
        "summary": {
            "passes": sum(1 for record in records if record["decision"] == "pass"),
            "warns": sum(1 for record in records if record["decision"] == "warn"),
            "fails": sum(1 for record in records if record["decision"] == "fail"),
        },
    }


def run_llmops_project() -> dict[str, object]:
    """Executa o pipeline completo sobre traces sinteticos."""

    evaluated = [evaluate_trace(enrich_trace(trace)) for trace in TRACE_DATA]
    return summarize_pipeline(evaluated)


def main() -> None:
    print(run_llmops_project())


if __name__ == "__main__":
    main()