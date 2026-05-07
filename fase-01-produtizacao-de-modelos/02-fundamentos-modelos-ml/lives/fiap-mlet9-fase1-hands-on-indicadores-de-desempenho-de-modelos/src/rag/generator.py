"""Geração de resposta com LLM."""

from langchain_openai import ChatOpenAI


def create_chat_model(model_name: str, api_key: str) -> ChatOpenAI:
    """Cria o cliente de chat da OpenAI.

    Args:
        model_name: Nome do modelo de chat.
        api_key: Chave da API OpenAI.

    Returns:
        Instância configurada do modelo de chat.
    """
    return ChatOpenAI(model=model_name, api_key=api_key, temperature=0)


def generate_answer(chat_model: ChatOpenAI, prompt: str) -> str:
    """Gera a resposta final do assistente.

    Args:
        chat_model: Modelo de chat configurado.
        prompt: Prompt completo com contexto.

    Returns:
        Texto da resposta gerada.
    """
    response = chat_model.invoke(prompt)
    return response.content.strip()
