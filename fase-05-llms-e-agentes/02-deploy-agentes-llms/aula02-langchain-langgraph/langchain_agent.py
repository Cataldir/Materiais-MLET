from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class ToolResult:
    """Resultado deterministico de uma tool local."""

    name: str
    output: str


@dataclass(frozen=True)
class ChainStep:
    """Representa uma etapa do fluxo sequencial."""

    stage: str
    detail: str


def run_tool(tool_name: str, query: str) -> ToolResult:
    """Executa tools locais sem qualquer dependencia externa."""

    tool_name = tool_name.lower()
    if tool_name == "calendar":
        return ToolResult("calendar", "Agenda local: reuniao de sprint as 14h.")
    if tool_name == "policy":
        return ToolResult("policy", "Politica local: reembolso permitido em ate 7 dias corridos.")
    if tool_name == "math":
        return ToolResult("math", "Resultado local: 4 tickets pendentes x 2 analistas = 8 slots.")
    return ToolResult("fallback", f"Sem tool especializada para: {query}")


def run_chain(query: str) -> dict[str, object]:
    """Executa um fluxo estilo LangChain com planner linear."""

    lower_query = query.lower()
    if "agenda" in lower_query or "reuniao" in lower_query:
        selected_tool = "calendar"
    elif "reembolso" in lower_query or "politica" in lower_query:
        selected_tool = "policy"
    else:
        selected_tool = "math"

    steps = [
        ChainStep("planner", f"Tool selecionada: {selected_tool}"),
        ChainStep("tool_call", f"Consulta enviada: {query}"),
    ]
    tool_result = run_tool(selected_tool, query)
    steps.append(ChainStep("synthesis", f"Resposta sintetizada a partir de {tool_result.name}"))
    return {
        "framework": "langchain_style",
        "selected_tool": selected_tool,
        "tool_result": asdict(tool_result),
        "steps": [asdict(step) for step in steps],
    }


def main() -> None:
    print(run_chain("Qual e a politica de reembolso para o curso?"))


if __name__ == "__main__":
    main()