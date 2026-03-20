from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol


@dataclass(frozen=True)
class AgentOutput:
    """Saida produzida por um agente especialista."""

    agent: str
    message: str


@dataclass(frozen=True)
class CoordinationReport:
    """Consolidacao da colaboracao multi-agent."""

    task: str
    outputs: list[AgentOutput]
    final_summary: str


class RoleAgent(Protocol):
    """PEP 544: contrato para agentes de papeis deterministas."""

    name: str

    def handle(self, task: str) -> AgentOutput:
        """Produz uma contribuicao local para a tarefa."""


class ResearchAgent:
    name = "research"

    def handle(self, task: str) -> AgentOutput:
        return AgentOutput(self.name, f"Fatos locais levantados para: {task}.")


class RiskAgent:
    name = "risk"

    def handle(self, task: str) -> AgentOutput:
        return AgentOutput(self.name, "Risco principal: falta de grounding e sobrecarga operacional.")


class WriterAgent:
    name = "writer"

    def handle(self, task: str) -> AgentOutput:
        return AgentOutput(self.name, "Resumo executivo redigido com foco em clareza e acao.")


class AgentMediator:
    """Mediator: controla a colaboracao entre especialistas."""

    def __init__(self, agents: list[RoleAgent]) -> None:
        self._agents = agents

    def coordinate(self, task: str) -> list[AgentOutput]:
        return [agent.handle(task) for agent in self._agents]


def run_multi_agent_demo(task: str = "Planejar rollout local do assistente") -> dict[str, object]:
    """Executa a orquestracao deterministica da aula."""

    mediator = AgentMediator([ResearchAgent(), RiskAgent(), WriterAgent()])
    outputs = mediator.coordinate(task)
    summary = " | ".join(output.message for output in outputs)
    report = CoordinationReport(task=task, outputs=outputs, final_summary=summary)
    return {
        "task": report.task,
        "outputs": [asdict(item) for item in report.outputs],
        "final_summary": report.final_summary,
    }


def main() -> None:
    print(run_multi_agent_demo())


if __name__ == "__main__":
    main()