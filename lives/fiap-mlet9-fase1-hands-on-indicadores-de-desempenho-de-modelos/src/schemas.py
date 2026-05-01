"""Estruturas de dados da aplicação."""

from dataclasses import asdict, dataclass, field
from typing import Any

from langchain_core.documents import Document


@dataclass
class AskRequest:
    """Representa a pergunta recebida pela API."""

    question: str


@dataclass
class EvaluationRecord:
    """Representa um registro persistido de evaluation."""

    timestamp: str
    question: str
    answer: str
    retrieved_documents: list[dict[str, Any]] = field(default_factory=list)
    evaluation: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Converte o registro para dicionário simples.

        Returns:
            Dicionário pronto para serialização em JSON.
        """
        return asdict(self)


def serialize_documents(documents: list[Document]) -> list[dict[str, Any]]:
    """Serializa documentos recuperados.

    Args:
        documents: Lista de documentos recuperados.

    Returns:
        Lista de documentos serializados.
    """
    serialized_documents = []
    for document in documents:
        serialized_documents.append(
            {
                "page_content": document.page_content,
                "metadata": document.metadata,
            }
        )
    return serialized_documents
