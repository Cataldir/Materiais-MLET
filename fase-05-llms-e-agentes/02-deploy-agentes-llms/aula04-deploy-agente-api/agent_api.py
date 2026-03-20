from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Protocol


@dataclass(frozen=True)
class AgentRequest:
    """Entrada principal do agente."""

    question: str
    channel: str = "local"


@dataclass(frozen=True)
class AgentResponse:
    """Resposta do agente com metadados minimos."""

    answer: str
    source: str
    trace_id: str


@dataclass(frozen=True)
class TraceEvent:
    """Evento de tracing em memoria."""

    trace_id: str
    stage: str
    detail: str


class PlannerPort(Protocol):
    """Porta para decidir a intencao da pergunta."""

    def select_topic(self, question: str) -> str:
        """Seleciona o topico dominante da pergunta."""


class KnowledgePort(Protocol):
    """Porta para recuperar conhecimento local."""

    def lookup(self, topic: str) -> str:
        """Recupera texto local para o topico informado."""


class TracePort(Protocol):
    """Porta para persistir traces localmente."""

    def record(self, event: TraceEvent) -> None:
        """Registra um evento."""

    def read_all(self) -> list[TraceEvent]:
        """Retorna todos os eventos gravados."""


class RulePlanner:
    """Strategy simples para mapear topicos por palavras-chave."""

    def select_topic(self, question: str) -> str:
        normalized = question.lower()
        if "reembolso" in normalized or "cancelamento" in normalized:
            return "billing"
        if "prazo" in normalized or "sprint" in normalized:
            return "operations"
        return "general"


class InMemoryKnowledgeBase:
    """Repositorio local com respostas curtas e deterministicas."""

    _ARTICLES = {
        "billing": "Reembolso local: permitido em ate 7 dias corridos apos a compra.",
        "operations": "Operacao local: o sprint fecha toda sexta as 17h com revisao tecnica.",
        "general": "Suporte local: abra um chamado interno com contexto e evidencias minimas.",
    }

    def lookup(self, topic: str) -> str:
        return self._ARTICLES[topic]


class InMemoryTraceStore:
    """Adapter local para trilhas de execucao."""

    def __init__(self) -> None:
        self._events: list[TraceEvent] = []

    def record(self, event: TraceEvent) -> None:
        self._events.append(event)

    def read_all(self) -> list[TraceEvent]:
        return list(self._events)


@dataclass
class SupportAgentService:
    """Facade de aplicacao sobre as portas hexagonais."""

    planner: PlannerPort
    knowledge: KnowledgePort
    traces: TracePort
    _trace_counter: int = field(default=0, init=False, repr=False)

    def answer(self, request: AgentRequest) -> AgentResponse:
        self._trace_counter += 1
        trace_id = f"trace-{self._trace_counter:03d}"
        topic = self.planner.select_topic(request.question)
        self.traces.record(TraceEvent(trace_id, "planner", topic))
        article = self.knowledge.lookup(topic)
        self.traces.record(TraceEvent(trace_id, "knowledge", article))
        answer = f"[{topic}] {article}"
        self.traces.record(TraceEvent(trace_id, "response", answer))
        return AgentResponse(answer=answer, source=topic, trace_id=trace_id)


def build_service() -> SupportAgentService:
    """Constroi o servico local reutilizavel em testes e API."""

    return SupportAgentService(
        planner=RulePlanner(),
        knowledge=InMemoryKnowledgeBase(),
        traces=InMemoryTraceStore(),
    )


def create_app() -> object:
    """Cria a app FastAPI se a dependencia estiver disponivel."""

    from fastapi import FastAPI

    service = build_service()
    app = FastAPI(title="local-agent-api", version="1.0.0")

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/ask")
    def ask(payload: dict[str, str]) -> dict[str, object]:
        response = service.answer(AgentRequest(question=payload["question"]))
        return asdict(response)

    @app.get("/traces")
    def traces() -> list[dict[str, str]]:
        return [asdict(event) for event in service.traces.read_all()]

    return app


def run_local_demo() -> dict[str, object]:
    """Executa a regra de negocio sem precisar subir servidor."""

    service = build_service()
    response = service.answer(AgentRequest(question="Qual e o prazo de sprint?"))
    return {
        "response": asdict(response),
        "traces": [asdict(event) for event in service.traces.read_all()],
    }


def main() -> None:
    print(run_local_demo())


if __name__ == "__main__":
    main()