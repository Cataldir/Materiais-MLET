"""Template de prompt do RAG."""

from langchain_core.documents import Document


def build_prompt(question: str, documents: list[Document]) -> str:
    """Monta o prompt com contexto recuperado.

    Args:
        question: Pergunta enviada pelo usuário.
        documents: Lista de documentos recuperados.

    Returns:
        Prompt final para geração.
    """
    context = "\n\n".join(document.page_content for document in documents)
    return (
        "Você é um assistente que responde usando apenas o contexto "
        "fornecido.\n\n"
        f"Contexto:\n{context}\n\n"
        f"Pergunta:\n{question}\n\n"
        "Responda de forma objetiva em português brasileiro."
    )
