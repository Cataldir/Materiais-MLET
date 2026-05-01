"""Leitura de arquivos da base de conhecimento."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_core.documents import Document


def load_pdf_documents(pdf_path: Path) -> list[Document]:
    """Carrega os documentos de um arquivo PDF.

    Args:
        pdf_path: Caminho do arquivo PDF.

    Returns:
        Lista de documentos carregados.
    """
    loader = PyPDFLoader(str(pdf_path))
    return loader.load()
