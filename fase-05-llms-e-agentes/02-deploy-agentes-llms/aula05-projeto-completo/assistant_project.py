from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class PlanStep:
    """Etapa planejada para responder ao usuario."""

    name: str
    rationale: str


@dataclass(frozen=True)
class RetrievalHit:
    """Documento local encontrado pelo retriever."""

    title: str
    content: str


@dataclass(frozen=True)
class AssistantReport:
    """Saida consolidada do projeto integrador."""

    query: str
    intent: str
    answer: str
    plan: list[PlanStep]
    hits: list[RetrievalHit]


class RuleBasedPlanner:
    """Builder-like role: monta um plano pequeno a partir da intencao."""

    def classify(self, query: str) -> str:
        lowered = query.lower()
        if "reembolso" in lowered:
            return "policy"
        if "agenda" in lowered or "sprint" in lowered:
            return "schedule"
        return "operations"

    def build(self, intent: str) -> list[PlanStep]:
        steps = [PlanStep("understand", f"Intencao inferida: {intent}")]
        if intent == "policy":
            steps.append(PlanStep("retrieve_policy", "Recuperar regra de negocio local"))
        elif intent == "schedule":
            steps.append(PlanStep("retrieve_schedule", "Consultar agenda interna local"))
        else:
            steps.append(PlanStep("run_tool", "Executar calculo operacional simples"))
        steps.append(PlanStep("compose", "Montar resposta final com evidencias locais"))
        return steps


class LocalRetriever:
    """Retriever local baseado em correspondencia explicita."""

    _DOCS = [
        RetrievalHit("politica_reembolso", "Reembolso pode ser solicitado em ate 7 dias corridos."),
        RetrievalHit("agenda_sprint", "Sprint local: planejamento na segunda e review na sexta."),
        RetrievalHit("capacidade_operacional", "Cada analista cobre 4 tickets por turno de suporte."),
    ]

    def search(self, intent: str) -> list[RetrievalHit]:
        if intent == "policy":
            return [self._DOCS[0]]
        if intent == "schedule":
            return [self._DOCS[1]]
        return [self._DOCS[2]]


class ToolRegistry:
    """No GoF pattern applies - registro simples e local de ferramentas seguras."""

    def run(self, intent: str, hits: list[RetrievalHit]) -> str:
        if intent == "operations":
            return "Capacidade projetada: 2 analistas x 4 tickets = 8 tickets por turno."
        return hits[0].content


def run_assistant_demo(query: str = "Qual e a politica de reembolso?") -> dict[str, object]:
    """Executa o fluxo completo do assistente local."""

    planner = RuleBasedPlanner()
    retriever = LocalRetriever()
    tools = ToolRegistry()
    intent = planner.classify(query)
    plan = planner.build(intent)
    hits = retriever.search(intent)
    answer = tools.run(intent, hits)
    report = AssistantReport(query=query, intent=intent, answer=answer, plan=plan, hits=hits)
    return {
        "query": report.query,
        "intent": report.intent,
        "answer": report.answer,
        "plan": [asdict(step) for step in report.plan],
        "hits": [asdict(hit) for hit in report.hits],
    }


def main() -> None:
    print(run_assistant_demo())


if __name__ == "__main__":
    main()