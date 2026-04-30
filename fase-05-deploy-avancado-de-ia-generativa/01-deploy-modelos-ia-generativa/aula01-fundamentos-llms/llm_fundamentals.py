"""LLM Fundamentals — fundamentos de Large Language Models.

Demonstra conceitos básicos de tokenização, geração de texto
e parâmetros de sampling usando a biblioteca transformers.

Requisitos:
    pip install transformers torch

Uso:
    python llm_fundamentals.py
"""

import logging
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def demonstrate_tokenization(text: str, model_name: str = "gpt2") -> dict[str, Any]:
    """Demonstra tokenização com diferentes modelos.

    Args:
        text: Texto a tokenizar.
        model_name: Nome do modelo HuggingFace.

    Returns:
        Dicionário com tokens, IDs e estatísticas.
    """
    try:
        from transformers import AutoTokenizer

        tokenizer = AutoTokenizer.from_pretrained(model_name)
        tokens = tokenizer.tokenize(text)
        token_ids = tokenizer.encode(text)

        result = {
            "text": text,
            "tokens": tokens,
            "token_ids": token_ids,
            "n_tokens": len(tokens),
            "vocab_size": tokenizer.vocab_size,
        }

        logger.info("Texto: '%s'", text)
        logger.info("Tokens (%d): %s", len(tokens), tokens)
        logger.info("Vocab size: %d", tokenizer.vocab_size)
        return result

    except ImportError:
        logger.warning("transformers não disponível. pip install transformers")
        words = text.split()
        tokens = [word for word in words]
        logger.info("Tokenização simples (por espaço): %d tokens", len(tokens))
        return {"text": text, "tokens": tokens, "n_tokens": len(tokens)}


def demonstrate_sampling_strategies() -> None:
    """Demonstra diferentes estratégias de sampling para geração de texto."""
    logger.info("\n=== Estratégias de Sampling em LLMs ===")

    strategies = {
        "Greedy": "Seleciona sempre o token de maior probabilidade. Determinístico, mas pode ser repetitivo.",
        "Temperature": "Temperatura > 1 → mais criativo/aleatório. Temperatura < 1 → mais conservador.",
        "Top-K": "Amostra apenas dos K tokens mais prováveis. K=50 é comum.",
        "Top-P (Nucleus)": "Amostra do menor conjunto de tokens cuja probabilidade acumulada >= p. p=0.9 é comum.",
        "Beam Search": "Mantém N sequências em paralelo e escolhe a de maior probabilidade conjunta.",
    }

    for name, description in strategies.items():
        logger.info("\n%s:", name)
        logger.info("  %s", description)


def generate_text(
    prompt: str,
    model_name: str = "gpt2",
    max_new_tokens: int = 50,
    temperature: float = 0.7,
    top_p: float = 0.9,
) -> str:
    """Gera texto usando modelo transformers com sampling configurável.

    Args:
        prompt: Texto inicial para geração.
        model_name: Nome do modelo HuggingFace.
        max_new_tokens: Número máximo de tokens a gerar.
        temperature: Temperatura de sampling (0.0-2.0).
        top_p: Threshold para nucleus sampling.

    Returns:
        Texto gerado pelo modelo.
    """
    try:
        import torch
        from transformers import pipeline

        generator = pipeline(
            "text-generation",
            model=model_name,
            device="cpu",
        )
        output = generator(
            prompt,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            do_sample=True,
            pad_token_id=50256,
        )
        generated = output[0]["generated_text"]
        logger.info("Prompt: '%s'", prompt)
        logger.info("Gerado: '%s'", generated)
        return generated

    except ImportError:
        logger.warning("transformers/torch não disponível")
        return f"[{prompt}... (simulado)]"


if __name__ == "__main__":
    logger.info("=== Demonstração de Tokenização ===")
    demonstrate_tokenization("Machine Learning Engineering is fascinating.")

    logger.info("\n=== Estratégias de Sampling ===")
    demonstrate_sampling_strategies()

    logger.info("\n=== Geração de Texto (requer GPU/modelo baixado) ===")
    logger.info("Exemplo de configuração de geração:")
    logger.info("  temperature=0.7, top_p=0.9, max_new_tokens=50")
