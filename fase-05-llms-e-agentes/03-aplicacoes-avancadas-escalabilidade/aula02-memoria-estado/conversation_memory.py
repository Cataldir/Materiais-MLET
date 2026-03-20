"""Conversation Memory — gerenciamento de memória e estado em conversas.

Implementa diferentes estratégias de memória para chatbots e agentes:
- Memória de janela (últimas N mensagens)
- Memória resumida (compressão automática)
- Memória por entidades (extração de fatos)

Uso:
    python conversation_memory.py
"""

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

_SUMMARY_CONTENT_TRUNCATE = 100


@dataclass
class Message:
    """Representa uma mensagem na conversa.

    Attributes:
        role: Papel do emissor ('user', 'assistant', 'system').
        content: Conteúdo da mensagem.
        timestamp: Data e hora da mensagem.
        metadata: Dados adicionais opcionais.
    """

    role: str
    content: str
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: dict[str, Any] = field(default_factory=dict)


class ConversationMemory(ABC):
    """Interface base para estratégias de memória de conversação."""

    @abstractmethod
    def add_message(self, role: str, content: str) -> None:
        """Adiciona uma mensagem à memória.

        Args:
            role: Papel do emissor.
            content: Conteúdo da mensagem.
        """

    @abstractmethod
    def get_context(self) -> list[dict[str, str]]:
        """Retorna o contexto formatado para o LLM.

        Returns:
            Lista de mensagens no formato {'role': ..., 'content': ...}.
        """

    @abstractmethod
    def clear(self) -> None:
        """Limpa toda a memória."""


class WindowMemory(ConversationMemory):
    """Memória de janela deslizante — mantém as últimas N mensagens.

    Attributes:
        window_size: Número máximo de mensagens a manter.
        messages: Lista de mensagens armazenadas.
    """

    def __init__(self, window_size: int = 10) -> None:
        """Inicializa memória de janela.

        Args:
            window_size: Número máximo de mensagens.
        """
        self.window_size = window_size
        self.messages: list[Message] = []

    def add_message(self, role: str, content: str) -> None:
        """Adiciona mensagem, removendo as mais antigas se necessário.

        Args:
            role: Papel do emissor.
            content: Conteúdo da mensagem.
        """
        self.messages.append(Message(role=role, content=content))
        if len(self.messages) > self.window_size:
            removed = self.messages.pop(0)
            logger.info("Mensagem mais antiga removida: '%s'", removed.content[:50])

    def get_context(self) -> list[dict[str, str]]:
        """Retorna mensagens na janela atual.

        Returns:
            Lista de mensagens formatadas.
        """
        return [{"role": m.role, "content": m.content} for m in self.messages]

    def clear(self) -> None:
        """Limpa todas as mensagens."""
        self.messages.clear()
        logger.info("Memória de janela limpa")


class SummaryMemory(ConversationMemory):
    """Memória com resumo automático — comprime mensagens antigas.

    Mantém um resumo do histórico antigo e as N mensagens mais recentes.

    Attributes:
        max_recent_messages: Mensagens recentes a manter intactas.
        summary: Resumo das mensagens comprimidas.
        recent_messages: Mensagens recentes não comprimidas.
    """

    def __init__(
        self,
        max_recent_messages: int = 5,
        summarize_fn: Any = None,
    ) -> None:
        """Inicializa memória com resumo.

        Args:
            max_recent_messages: Quantas mensagens manter sem compressão.
            summarize_fn: Função para resumir o histórico (LLM ou regra).
        """
        self.max_recent_messages = max_recent_messages
        self.summarize_fn = summarize_fn or self._default_summarize
        self.summary: str = ""
        self.recent_messages: list[Message] = []

    def _default_summarize(self, messages: list[Message]) -> str:
        """Resumo padrão: concatena as mensagens com indicação de troca.

        Args:
            messages: Mensagens a resumir.

        Returns:
            Resumo textual do histórico.
        """
        lines = [f"{m.role}: {m.content[:_SUMMARY_CONTENT_TRUNCATE]}" for m in messages]
        return "Histórico anterior: " + " | ".join(lines)

    def add_message(self, role: str, content: str) -> None:
        """Adiciona mensagem e comprime histórico se necessário.

        Args:
            role: Papel do emissor.
            content: Conteúdo da mensagem.
        """
        self.recent_messages.append(Message(role=role, content=content))

        if len(self.recent_messages) > self.max_recent_messages:
            messages_to_compress = self.recent_messages[: -self.max_recent_messages]
            new_summary = self.summarize_fn(messages_to_compress)
            self.summary = (self.summary + "\n" + new_summary).strip()
            self.recent_messages = self.recent_messages[-self.max_recent_messages :]
            logger.info("Histórico comprimido. Resumo: '%s'", self.summary[:100])

    def get_context(self) -> list[dict[str, str]]:
        """Retorna contexto com resumo + mensagens recentes.

        Returns:
            Lista com mensagem de resumo (se houver) + mensagens recentes.
        """
        context = []
        if self.summary:
            context.append(
                {"role": "system", "content": f"Contexto anterior: {self.summary}"}
            )
        context.extend(
            [{"role": m.role, "content": m.content} for m in self.recent_messages]
        )
        return context

    def clear(self) -> None:
        """Limpa memória e resumo."""
        self.summary = ""
        self.recent_messages.clear()


def demo_conversation_memory() -> None:
    """Demonstra as estratégias de memória em conversas simuladas."""
    logger.info("=== Window Memory (5 mensagens) ===")
    window_mem = WindowMemory(window_size=5)

    conversations = [
        ("user", "Olá! Como você pode me ajudar?"),
        ("assistant", "Posso ajudar com ML, Python e deploy de modelos."),
        ("user", "Explique Random Forest."),
        ("assistant", "Random Forest é um ensemble de árvores de decisão."),
        ("user", "E XGBoost?"),
        (
            "assistant",
            "XGBoost usa gradient boosting para treinar árvores sequencialmente.",
        ),
        ("user", "Qual é mais rápido?"),
    ]

    for role, content in conversations:
        window_mem.add_message(role, content)

    context = window_mem.get_context()
    logger.info("Contexto atual (%d mensagens):", len(context))
    for msg in context:
        logger.info("  %s: %s", msg["role"], msg["content"][:80])

    logger.info("\n=== Summary Memory (max 3 recentes) ===")
    summary_mem = SummaryMemory(max_recent_messages=3)
    for role, content in conversations:
        summary_mem.add_message(role, content)

    context_summary = summary_mem.get_context()
    logger.info("Contexto com resumo (%d entradas):", len(context_summary))
    for msg in context_summary:
        logger.info("  %s: %s", msg["role"], msg["content"][:100])


if __name__ == "__main__":
    demo_conversation_memory()
