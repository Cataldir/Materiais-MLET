"""Tracing local inspirado em OpenTelemetry para pipelines de ML.

Uso:
    python otel_tracing.py
"""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class TraceSpan:
    span_id: str
    name: str
    parent_id: str | None
    duration_ms: float
    status: str
    attributes: dict[str, str]


def create_span(
    name: str,
    duration_ms: float,
    parent_id: str | None = None,
    attributes: dict[str, str] | None = None,
) -> TraceSpan:
    """Cria um span local com atributos estaveis para walkthroughs didaticos."""
    return TraceSpan(
        span_id=f"span-{name}",
        name=name,
        parent_id=parent_id,
        duration_ms=duration_ms,
        status="ok",
        attributes=attributes or {},
    )


def build_demo_trace() -> list[TraceSpan]:
    # Decorator-like concern: tracing descreve o pipeline sem alterar a logica de negocio.
    root_id = "trace-demo"
    return [
        create_span("ingest", 12.0, parent_id=root_id, attributes={"rows": "240"}),
        create_span("transform", 18.0, parent_id=root_id, attributes={"features": "8"}),
        create_span(
            "train", 42.0, parent_id=root_id, attributes={"model": "random_forest"}
        ),
    ]


def summarize_trace(spans: list[TraceSpan]) -> dict[str, object]:
    return {
        "span_count": len(spans),
        "span_names": [span.name for span in spans],
        "total_duration_ms": round(sum(span.duration_ms for span in spans), 1),
        "root_parent": spans[0].parent_id if spans else None,
    }


def run_demo_pipeline() -> dict[str, object]:
    spans = build_demo_trace()
    return {
        "spans": [asdict(span) for span in spans],
        "summary": summarize_trace(spans),
    }


def main() -> None:
    results = run_demo_pipeline()
    print("Tracing local para pipeline de ML\n")
    for span in results["spans"]:
        print(
            f"- {span['name']}: {span['duration_ms']:.1f}ms | attrs={span['attributes']}"
        )
    print("\nResumo")
    print(results["summary"])


if __name__ == "__main__":
    main()
