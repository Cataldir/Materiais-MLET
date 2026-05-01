"""Recuperação de documentos no Chroma."""

from langchain_chroma import Chroma
from langchain_core.documents import Document


def retrieve_documents(
    vector_store: Chroma,
    question: str,
    top_k: int,
) -> list[Document]:
    """Recupera os documentos mais relevantes.

    Args:
        vector_store: Banco vetorial configurado.
        question: Pergunta enviada pelo usuário.
        top_k: Quantidade de documentos a recuperar.

    Returns:
        Lista de documentos recuperados.
    """
    return vector_store.similarity_search(question, k=top_k)
