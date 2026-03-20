from __future__ import annotations

from dataclasses import asdict, dataclass

from langchain_agent import run_chain, run_tool


@dataclass(frozen=True)
class GraphTransition:
    """Transicao observavel entre nos do grafo."""

    source: str
    target: str
    reason: str


def route_query(query: str) -> str:
    """Router local baseado em regras declarativas."""

    normalized = query.lower()
    if "agenda" in normalized or "reuniao" in normalized:
        return "calendar"
    if "reembolso" in normalized or "politica" in normalized:
        return "policy"
    return "math"


def run_graph(query: str) -> dict[str, object]:
    """Executa um fluxo estilo LangGraph com roteamento explicito."""

    route = route_query(query)
    transitions = [
        GraphTransition("input", "router", "Entrada recebida"),
        GraphTransition("router", route, f"Rota escolhida para consulta: {query}"),
        GraphTransition(route, "final", "Tool concluiu execucao"),
    ]
    tool_result = run_tool(route, query)
    return {
        "framework": "langgraph_style",
        "route": route,
        "visited_nodes": ["input", "router", route, "final"],
        "tool_result": asdict(tool_result),
        "transitions": [asdict(item) for item in transitions],
    }


def compare_workflows(query: str) -> dict[str, object]:
    """Compara os dois estilos mantendo a mesma base de tools."""

    chain_report = run_chain(query)
    graph_report = run_graph(query)
    return {
        "query": query,
        "langchain": chain_report,
        "langgraph": graph_report,
    }


def main() -> None:
    print(compare_workflows("Qual e a agenda local de reunioes hoje?"))


if __name__ == "__main__":
    main()