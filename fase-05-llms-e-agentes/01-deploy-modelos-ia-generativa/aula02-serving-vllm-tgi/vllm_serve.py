"""vLLM Serving — servidor de inferência de alta performance para LLMs.

Demonstra como servir LLMs com vLLM para inferência em produção,
incluindo configuração de parâmetros, batching e API OpenAI-compatible.

Requisitos:
    pip install vllm  # Requer GPU NVIDIA com CUDA

Uso:
    # Iniciar servidor vLLM
    python -m vllm.entrypoints.openai.api_server \
        --model mistralai/Mistral-7B-Instruct-v0.2 \
        --port 8000

    # Ou via script:
    python vllm_serve.py --model microsoft/Phi-3-mini-4k-instruct
"""

import argparse
import logging
import os
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

DEFAULT_MODEL = "microsoft/Phi-3-mini-4k-instruct"
DEFAULT_PORT = 8000
DEFAULT_MAX_MODEL_LEN = 4096


def start_vllm_server(
    model_name: str,
    port: int = DEFAULT_PORT,
    max_model_len: int = DEFAULT_MAX_MODEL_LEN,
    gpu_memory_utilization: float = 0.85,
    tensor_parallel_size: int = 1,
) -> None:
    """Inicia servidor vLLM com configurações otimizadas.

    Args:
        model_name: Nome ou caminho do modelo HuggingFace.
        port: Porta do servidor HTTP.
        max_model_len: Comprimento máximo de contexto.
        gpu_memory_utilization: Fração da GPU a usar (0.0-1.0).
        tensor_parallel_size: Número de GPUs para paralelismo de tensor.
    """
    try:
        from vllm.entrypoints.openai.api_server import run_server
        from vllm.engine.arg_utils import AsyncEngineArgs

        engine_args = AsyncEngineArgs(
            model=model_name,
            max_model_len=max_model_len,
            gpu_memory_utilization=gpu_memory_utilization,
            tensor_parallel_size=tensor_parallel_size,
            trust_remote_code=True,
        )
        logger.info("Iniciando vLLM com modelo: %s na porta %d", model_name, port)
        run_server(engine_args, host="0.0.0.0", port=port)

    except ImportError:
        logger.warning("vLLM não instalado. Requer GPU + pip install vllm")
        logger.info("Configurações que seriam usadas:")
        logger.info("  Modelo: %s", model_name)
        logger.info("  Porta: %d", port)
        logger.info("  Max context: %d tokens", max_model_len)
        logger.info("  GPU utilization: %.0f%%", gpu_memory_utilization * 100)


def query_vllm_api(
    prompt: str,
    model: str = DEFAULT_MODEL,
    base_url: str = "http://localhost:8000",
    max_tokens: int = 256,
    temperature: float = 0.7,
) -> str:
    """Consulta API OpenAI-compatible do vLLM.

    Args:
        prompt: Prompt para o modelo.
        model: Nome do modelo (deve corresponder ao servido).
        base_url: URL base do servidor vLLM.
        max_tokens: Máximo de tokens a gerar.
        temperature: Temperatura de sampling.

    Returns:
        Resposta gerada pelo modelo.
    """
    try:
        from openai import OpenAI

        client = OpenAI(api_key="not-required", base_url=f"{base_url}/v1")
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content or ""
    except ImportError:
        logger.warning("openai não instalado. pip install openai")
        return "[Resposta simulada]"
    except Exception as exc:
        logger.error("Falha ao consultar vLLM: %s", exc)
        return ""


def main() -> None:
    """Entry point CLI para iniciar servidor vLLM."""
    parser = argparse.ArgumentParser(description="Servidor vLLM para LLMs")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL)
    parser.add_argument("--port", type=int, default=DEFAULT_PORT)
    parser.add_argument("--max-model-len", type=int, default=DEFAULT_MAX_MODEL_LEN)
    parser.add_argument("--gpu-memory", type=float, default=0.85)
    parser.add_argument("--tensor-parallel", type=int, default=1)
    args = parser.parse_args()

    start_vllm_server(
        args.model, args.port, args.max_model_len,
        args.gpu_memory, args.tensor_parallel
    )


if __name__ == "__main__":
    main()
