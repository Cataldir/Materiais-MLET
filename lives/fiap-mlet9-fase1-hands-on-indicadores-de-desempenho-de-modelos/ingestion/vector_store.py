"""Acesso ao ChromaDB."""

from pathlib import Path

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import OpenAIEmbeddings


def create_vector_store(
    collection_name: str,
    persist_directory: Path,
    embeddings: OpenAIEmbeddings,
) -> Chroma:
    """Cria ou abre o banco vetorial local.

    Args:
        collection_name: Nome da coleção do Chroma.
        persist_directory: Diretório de persistência local.
        embeddings: Cliente de embeddings.

    Returns:
        Instância do banco vetorial.
    """
    return Chroma(
        collection_name=collection_name,
        embedding_function=embeddings,
        persist_directory=str(persist_directory),
    )


def add_documents(
    vector_store: Chroma,
    documents: list[Document],
) -> None:
    """Adiciona documentos ao banco vetorial.

    Args:
        vector_store: Instância do banco vetorial.
        documents: Lista de documentos ou chunks.
    """
    vector_store.add_documents(documents)
