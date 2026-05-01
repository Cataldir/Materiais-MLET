"""Orquestração simples do pipeline RAG."""

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI

from src.rag.generator import generate_answer
from src.rag.prompt import build_prompt
from src.rag.retriever import retrieve_documents


def answer_question(
    vector_store: Chroma,
    chat_model: ChatOpenAI,
    question: str,
    top_k: int,
) -> tuple[str, list[Document]]:
    """Executa retrieval e generation.

    Args:
        vector_store: Banco vetorial configurado.
        chat_model: Modelo de chat configurado.
        question: Pergunta enviada pelo usuário.
        top_k: Quantidade de documentos a recuperar.

    Returns:
        Tupla com resposta gerada e documentos recuperados.
    """
    documents = retrieve_documents(vector_store, question, top_k)
    prompt = build_prompt(question, documents)
    answer = generate_answer(chat_model, prompt)
    return answer, documents
