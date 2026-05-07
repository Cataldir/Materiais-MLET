"""Configuração de embeddings."""

import os

from langchain_openai import OpenAIEmbeddings


def create_embeddings(model_name: str) -> OpenAIEmbeddings:
    """Cria o cliente de embeddings da OpenAI.

    Args:
        model_name: Nome do modelo de embeddings.

    Returns:
        Instância configurada do cliente de embeddings.
    """
    api_key = os.getenv("OPENAI_API_KEY") or os.getenv("OPEN_AI_KEY")
    return OpenAIEmbeddings(model=model_name, api_key=api_key)
