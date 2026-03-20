from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class LLMTraceStep:
    name: str
    latency_ms: float
    tokens: int
    metadata: dict[str, str]


def build_rag_trace() -> list[LLMTraceStep]:
    # Facade-like role: uma interface unica resume diferentes etapas de tracing do fluxo generativo.
    return [
        LLMTraceStep("retrieve", latency_ms=24.0, tokens=0, metadata={"chunks": "1"}),
        LLMTraceStep("build_prompt", latency_ms=8.0, tokens=180, metadata={"template": "support_rag"}),
        LLMTraceStep("generate", latency_ms=91.0, tokens=240, metadata={"model": "mock-llm"}),
        LLMTraceStep("evaluate", latency_ms=17.0, tokens=60, metadata={"grounded": "false"}),
    ]


def compute_trace_metrics(trace_steps: list[LLMTraceStep]) -> dict[str, float]:
    total_tokens = sum(step.tokens for step in trace_steps)
    total_latency_ms = round(sum(step.latency_ms for step in trace_steps), 1)
    estimated_cost_usd = round(total_tokens * 0.000002, 6)
    return {
        "total_tokens": float(total_tokens),
        "total_latency_ms": total_latency_ms,
        "estimated_cost_usd": estimated_cost_usd,
    }


def flag_llmops_risks(
    trace_steps: list[LLMTraceStep],
    metrics: dict[str, float],
) -> list[str]:
    risks: list[str] = []
    retrieve_step = next(step for step in trace_steps if step.name == "retrieve")
    evaluate_step = next(step for step in trace_steps if step.name == "evaluate")
    if retrieve_step.metadata.get("chunks") == "1" or evaluate_step.metadata.get("grounded") == "false":
        risks.append("weak_grounding")
    if metrics["total_latency_ms"] >= 120.0:
        risks.append("latency_attention")
    return risks


def run_llmops_trace_demo() -> dict[str, object]:
    trace_steps = build_rag_trace()
    metrics = compute_trace_metrics(trace_steps)
    risks = flag_llmops_risks(trace_steps, metrics)
    return {
        "trace": [asdict(step) for step in trace_steps],
        "metrics": metrics,
        "risks": risks,
    }


def main() -> None:
    results = run_llmops_trace_demo()
    print("Tracing local para LLMOps\n")
    print(results["metrics"])
    print(results["risks"])


if __name__ == "__main__":
    main()