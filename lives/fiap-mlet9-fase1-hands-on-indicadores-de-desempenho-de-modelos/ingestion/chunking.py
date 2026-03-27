"""Funções para chunking dos documentos."""

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split_documents(
    documents: list[Document],
    chunk_size: int,
    chunk_overlap: int,
) -> list[Document]:
    """Divide documentos em chunks menores.

    Args:
        documents: Lista de documentos originais.
        chunk_size: Tamanho máximo de cada chunk.
        chunk_overlap: Sobreposição entre chunks.

    Returns:
        Lista de chunks gerados.
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
    )
    return splitter.split_documents(documents)
