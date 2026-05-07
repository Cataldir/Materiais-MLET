"""Avaliação da resposta gerada."""

from functools import lru_cache
from typing import Any, Callable

from langchain_openai import ChatOpenAI

from src.config import EVAL_MODEL, OPENAI_API_KEY


def _fallback_metric(reason: str) -> dict[str, Any]:
    """Monta um resultado simples quando a métrica não estiver disponível.

    Args:
        reason: Motivo do fallback.

    Returns:
        Dicionário com o resultado da métrica.
    """
    return {"score": None, "reason": reason}


def _normalize_result(result: Any) -> dict[str, Any]:
    """Normaliza o retorno do evaluator para JSON simples.

    Args:
        result: Resultado retornado pelo evaluator.

    Returns:
        Dicionário serializável com score e reason.
    """
    if isinstance(result, dict):
        score = result.get("score")
        reason = result.get("reasoning") or result.get("comment")
        normalized = {"score": score, "reason": reason}
        for key, value in result.items():
            if key not in {"score", "reasoning", "comment"}:
                normalized[key] = value
        return normalized
    return {"score": result, "reason": None}


def _run_metric(
    metric_name: str,
    evaluator: Callable[..., Any] | None,
    **kwargs: Any,
) -> dict[str, Any]:
    """Executa uma métrica de forma segura.

    Args:
        metric_name: Nome da métrica.
        evaluator: Função da métrica.
        **kwargs: Argumentos aceitos pelo evaluator.

    Returns:
        Resultado serializável da métrica.
    """
    if evaluator is None or not callable(evaluator):
        return _fallback_metric(
            f"Métrica '{metric_name}' indisponível na instalação atual."
        )

    try:
        result = evaluator(**kwargs)
    except Exception as error:
        return _fallback_metric(str(error))

    return _normalize_result(result)


@lru_cache(maxsize=1)
def _create_judge() -> ChatOpenAI | None:
    """Cria o modelo juiz para evaluation.

    Returns:
        Modelo de chat configurado ou `None` se faltar a chave.
    """
    if not OPENAI_API_KEY:
        return None
    return ChatOpenAI(
        model=EVAL_MODEL,
        api_key=OPENAI_API_KEY,
        temperature=0,
    )


@lru_cache(maxsize=1)
def _load_evaluators() -> dict[str, Callable[..., Any] | None]:
    """Cria os evaluators do OpenEvals.

    Returns:
        Dicionário com os evaluators prontos.
    """
    judge = _create_judge()
    if judge is None:
        return {
            "groundedness": None,
            "helpfulness": None,
            "retrieval_relevance": None,
        }

    try:
        from openevals import create_llm_as_judge
        from openevals.prompts import (
            RAG_GROUNDEDNESS_PROMPT,
            RAG_HELPFULNESS_PROMPT,
            RAG_RETRIEVAL_RELEVANCE_PROMPT,
        )
    except ImportError:
        return {
            "groundedness": None,
            "helpfulness": None,
            "retrieval_relevance": None,
        }

    return {
        "groundedness": create_llm_as_judge(
            prompt=RAG_GROUNDEDNESS_PROMPT,
            judge=judge,
            continuous=True
        ),
        "helpfulness": create_llm_as_judge(
            prompt=RAG_HELPFULNESS_PROMPT,
            judge=judge,
            continuous=True
        ),
        "retrieval_relevance": create_llm_as_judge(
            prompt=RAG_RETRIEVAL_RELEVANCE_PROMPT,
            judge=judge,
            continuous=True
        ),
    }


def evaluate_answer(
    question: str,
    answer: str,
    retrieved_documents: list[dict[str, Any]],
) -> dict[str, Any]:
    """Executa as métricas da biblioteca OpenEvals.

    Args:
        question: Pergunta enviada pelo usuário.
        answer: Resposta gerada pelo modelo.
        retrieved_documents: Documentos recuperados serializados.

    Returns:
        Dicionário com os resultados de evaluation.
    """
    context = "\n\n".join(
        document["page_content"] for document in retrieved_documents
    )

    evaluators = _load_evaluators()

    return {
        "groundedness": _run_metric(
            "groundedness",
            evaluators["groundedness"],
            outputs=answer,
            context=context,
        ),
        "helpfulness": _run_metric(
            "helpfulness",
            evaluators["helpfulness"],
            inputs=question,
            outputs=answer,
        ),
        "retrieval_relevance": _run_metric(
            "retrieval_relevance",
            evaluators["retrieval_relevance"],
            inputs=question,
            context=context,
        ),
    }
