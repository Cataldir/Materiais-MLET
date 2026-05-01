"""Script para construir o índice vetorial local."""

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from ingestion.chunking import split_documents
from ingestion.embeddings import create_embeddings
from ingestion.loaders import load_pdf_documents
from ingestion.vector_store import add_documents, create_vector_store
from src.config import (
    CHROMA_COLLECTION_NAME,
    CHROMA_DIRECTORY,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
    KNOWLEDGE_BASE_PATH,
)


def build_index() -> int:
    """Executa o fluxo de ingestão da base vetorial.

    Returns:
        Quantidade de chunks enviados ao Chroma.
    """
    documents = load_pdf_documents(KNOWLEDGE_BASE_PATH)
    chunks = split_documents(documents, CHUNK_SIZE, CHUNK_OVERLAP)
    embeddings = create_embeddings(EMBEDDING_MODEL)
    vector_store = create_vector_store(
        collection_name=CHROMA_COLLECTION_NAME,
        persist_directory=CHROMA_DIRECTORY,
        embeddings=embeddings,
    )
    add_documents(vector_store, chunks)
    return len(chunks)


def main() -> None:
    """Executa a construção do índice."""
    total_chunks = build_index()
    print(f"Índice gerado com {total_chunks} chunks.")


if __name__ == "__main__":
    main()
