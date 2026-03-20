"""Cost Tracker — rastreamento de custo e latência em chamadas a LLMs.

Demonstra como monitorar e otimizar o uso de APIs de LLMs,
rastreando tokens consumidos, custo e latência por chamada.

Uso:
    python cost_tracker.py
"""

import logging
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PRICING = {
    "gpt-4-turbo": {"input": 0.01, "output": 0.03},
    "gpt-4o": {"input": 0.005, "output": 0.015},
    "gpt-3.5-turbo": {"input": 0.001, "output": 0.002},
    "claude-3-opus": {"input": 0.015, "output": 0.075},
    "claude-3-sonnet": {"input": 0.003, "output": 0.015},
}


@dataclass
class LLMCallRecord:
    """Registro de uma chamada a LLM.

    Attributes:
        timestamp: Data e hora da chamada.
        model: Modelo utilizado.
        input_tokens: Tokens de entrada.
        output_tokens: Tokens de saída.
        latency_ms: Latência em milissegundos.
        cost_usd: Custo estimado em USD.
        success: Se a chamada foi bem-sucedida.
        error: Mensagem de erro (se houver).
    """

    timestamp: datetime
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: float
    cost_usd: float
    success: bool = True
    error: str = ""


@dataclass
class CostTracker:
    """Rastreador de custo e uso de APIs de LLM.

    Attributes:
        records: Histórico de chamadas registradas.
        budget_limit_usd: Limite de orçamento (0 = sem limite).
    """

    records: list[LLMCallRecord] = field(default_factory=list)
    budget_limit_usd: float = 0.0

    def record_call(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: float,
        success: bool = True,
        error: str = "",
    ) -> LLMCallRecord:
        """Registra uma chamada à API do LLM.

        Args:
            model: Nome do modelo.
            input_tokens: Tokens consumidos no input.
            output_tokens: Tokens gerados no output.
            latency_ms: Latência em ms.
            success: Se foi bem-sucedida.
            error: Mensagem de erro opcional.

        Returns:
            Registro criado.
        """
        pricing = PRICING.get(model, {"input": 0.001, "output": 0.002})
        cost = (
            input_tokens * pricing["input"] + output_tokens * pricing["output"]
        ) / 1000

        record = LLMCallRecord(
            timestamp=datetime.now(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost,
            success=success,
            error=error,
        )
        self.records.append(record)

        if self.budget_limit_usd > 0:
            total_cost = self.total_cost
            if total_cost > self.budget_limit_usd:
                logger.warning(
                    "⚠️  Limite de orçamento atingido: $%.4f / $%.4f",
                    total_cost,
                    self.budget_limit_usd,
                )

        return record

    @property
    def total_cost(self) -> float:
        """Custo total acumulado em USD."""
        return sum(r.cost_usd for r in self.records)

    @property
    def total_tokens(self) -> dict[str, int]:
        """Total de tokens consumidos (input + output)."""
        return {
            "input": sum(r.input_tokens for r in self.records),
            "output": sum(r.output_tokens for r in self.records),
        }

    @property
    def avg_latency_ms(self) -> float:
        """Latência média em ms."""
        if not self.records:
            return 0.0
        return float(sum(r.latency_ms for r in self.records) / len(self.records))

    def summary(self) -> dict[str, Any]:
        """Gera resumo do uso.

        Returns:
            Dicionário com estatísticas de uso e custo.
        """
        by_model: dict[str, dict[str, Any]] = {}
        for r in self.records:
            if r.model not in by_model:
                by_model[r.model] = {"calls": 0, "cost": 0.0, "tokens": 0}
            by_model[r.model]["calls"] += 1
            by_model[r.model]["cost"] += r.cost_usd
            by_model[r.model]["tokens"] += r.input_tokens + r.output_tokens

        summary_data = {
            "total_calls": len(self.records),
            "total_cost_usd": self.total_cost,
            "total_tokens": self.total_tokens,
            "avg_latency_ms": self.avg_latency_ms,
            "by_model": by_model,
        }

        logger.info("=== Cost Tracker Summary ===")
        logger.info("Total de chamadas: %d", summary_data["total_calls"])
        logger.info("Custo total: $%.6f", summary_data["total_cost_usd"])
        logger.info(
            "Tokens totais: input=%d, output=%d", **summary_data["total_tokens"]
        )
        logger.info("Latência média: %.1fms", summary_data["avg_latency_ms"])

        for model, stats in by_model.items():
            logger.info(
                "  %s: %d calls, $%.6f, %d tokens",
                model,
                stats["calls"],
                stats["cost"],
                stats["tokens"],
            )

        return summary_data


def tracked_llm_call(
    tracker: CostTracker,
    model: str,
    llm_fn: Callable[[str], tuple[str, int, int]],
    prompt: str,
) -> str:
    """Wrapper para chamadas a LLM com rastreamento automático.

    Args:
        tracker: Instância do CostTracker.
        model: Nome do modelo a chamar.
        llm_fn: Função que retorna (resposta, input_tokens, output_tokens).
        prompt: Prompt para o LLM.

    Returns:
        Resposta do LLM.
    """
    start = time.perf_counter()
    try:
        response, input_tokens, output_tokens = llm_fn(prompt)
        latency = (time.perf_counter() - start) * 1000
        tracker.record_call(model, input_tokens, output_tokens, latency)
        return response
    except Exception as exc:
        latency = (time.perf_counter() - start) * 1000
        tracker.record_call(model, 0, 0, latency, success=False, error=str(exc))
        raise


def demo_cost_tracking() -> None:
    """Demonstra rastreamento de custos com chamadas simuladas."""
    tracker = CostTracker(budget_limit_usd=0.10)

    def mock_gpt4(prompt: str) -> tuple[str, int, int]:
        time.sleep(0.01)
        input_tokens = len(prompt.split()) * 2
        output_tokens = 150
        return "Resposta simulada do GPT-4.", input_tokens, output_tokens

    def mock_gpt35(prompt: str) -> tuple[str, int, int]:
        time.sleep(0.005)
        input_tokens = len(prompt.split()) * 2
        output_tokens = 100
        return "Resposta simulada do GPT-3.5.", input_tokens, output_tokens

    prompts = [
        "Explique o que é Machine Learning.",
        "Como fazer deploy de um modelo com Docker?",
        "O que é RAG em LLMs?",
    ]

    for prompt in prompts:
        tracked_llm_call(tracker, "gpt-4-turbo", mock_gpt4, prompt)
        tracked_llm_call(tracker, "gpt-3.5-turbo", mock_gpt35, prompt)

    tracker.summary()


if __name__ == "__main__":
    demo_cost_tracking()
