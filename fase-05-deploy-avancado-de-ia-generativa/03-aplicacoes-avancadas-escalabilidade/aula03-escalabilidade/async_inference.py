"""Simula tradeoffs de escalabilidade para geracao de texto mockada.

O backend nao depende de modelos reais. Em vez disso, usamos um custo modelado
por lote para comparar estrategias assicronas de atendimento.
"""

from __future__ import annotations

import asyncio
import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class GenerationRequest:
    """Representa uma requisicao de texto sintetica."""

    request_id: int
    prompt: str
    max_tokens: int = 48


@dataclass(frozen=True)
class GenerationResponse:
    """Resposta mockada do backend."""

    request_id: int
    content: str


@dataclass(frozen=True)
class BackendConfig:
    """Parametros de custo do backend mockado."""

    base_batch_ms: float = 24.0
    per_item_ms: float = 5.0


@dataclass(frozen=True)
class StrategyExecution:
    """Resultado bruto para calculo do resumo final."""

    responses: tuple[GenerationResponse, ...]
    batch_sizes: tuple[int, ...]
    worker_count: int
    per_batch_overhead_ms: float = 0.0


@dataclass(frozen=True)
class ScalingSummary:
    """Resumo comparativo de uma estrategia de escalabilidade."""

    strategy: str
    processed_requests: int
    batches_processed: int
    total_time_ms: float
    average_latency_ms: float
    throughput_rps: float


class MockTextGenerationBackend:
    """Backend local que gera respostas deterministicas."""

    def __init__(self, config: BackendConfig | None = None) -> None:
        self.config = config or BackendConfig()

    async def generate(
        self, requests: Sequence[GenerationRequest]
    ) -> tuple[GenerationResponse, ...]:
        await asyncio.sleep(0)
        return tuple(
            GenerationResponse(
                request_id=request.request_id,
                content=f"mock-response-{request.request_id}: {request.prompt[:24]}",
            )
            for request in requests
        )

    def cost_for_batch(self, batch_size: int) -> float:
        return self.config.base_batch_ms + self.config.per_item_ms * batch_size


class ScalingStrategy(Protocol):
    """Contrato comum para estrategias de atendimento."""

    name: str

    async def execute(
        self,
        backend: MockTextGenerationBackend,
        requests: Sequence[GenerationRequest],
    ) -> StrategyExecution:
        """Processa a lista de requests usando o backend mockado."""


class AsyncDirectStrategy:
    """Dispara requests assincornas diretamente ao backend."""

    name = "async_direct"

    def __init__(self, concurrency: int = 4) -> None:
        self.concurrency = concurrency

    async def execute(
        self,
        backend: MockTextGenerationBackend,
        requests: Sequence[GenerationRequest],
    ) -> StrategyExecution:
        semaphore = asyncio.Semaphore(self.concurrency)
        responses: list[GenerationResponse] = []

        async def invoke(request: GenerationRequest) -> None:
            async with semaphore:
                result = await backend.generate([request])
                responses.extend(result)

        await asyncio.gather(*(invoke(request) for request in requests))
        return StrategyExecution(
            responses=tuple(
                sorted(responses, key=lambda response: response.request_id)
            ),
            batch_sizes=tuple(1 for _ in requests),
            worker_count=self.concurrency,
        )


class QueuedWorkersStrategy:
    """Usa fila assincorna para limitar ingestao e processamento."""

    name = "queued_workers"

    def __init__(self, worker_count: int = 3, queue_size: int = 8) -> None:
        self.worker_count = worker_count
        self.queue_size = queue_size

    async def execute(
        self,
        backend: MockTextGenerationBackend,
        requests: Sequence[GenerationRequest],
    ) -> StrategyExecution:
        queue: asyncio.Queue[GenerationRequest] = asyncio.Queue(maxsize=self.queue_size)
        producer_done = asyncio.Event()
        responses: list[GenerationResponse] = []

        async def producer() -> None:
            for request in requests:
                await queue.put(request)
            producer_done.set()

        async def worker() -> None:
            while True:
                try:
                    request = await asyncio.wait_for(queue.get(), timeout=0.01)
                except TimeoutError:
                    if producer_done.is_set() and queue.empty():
                        return
                    continue
                result = await backend.generate([request])
                responses.extend(result)
                queue.task_done()

        producer_task = asyncio.create_task(producer())
        workers = [asyncio.create_task(worker()) for _ in range(self.worker_count)]
        await producer_task
        await queue.join()
        await asyncio.gather(*workers)
        return StrategyExecution(
            responses=tuple(
                sorted(responses, key=lambda response: response.request_id)
            ),
            batch_sizes=tuple(1 for _ in requests),
            worker_count=self.worker_count,
            per_batch_overhead_ms=3.0,
        )


class AsyncBatchingStrategy:
    """Agrupa requests de uma fila em lotes maiores."""

    name = "async_batching"

    def __init__(self, worker_count: int = 2, batch_size: int = 5) -> None:
        self.worker_count = worker_count
        self.batch_size = batch_size

    async def execute(
        self,
        backend: MockTextGenerationBackend,
        requests: Sequence[GenerationRequest],
    ) -> StrategyExecution:
        queue: asyncio.Queue[GenerationRequest] = asyncio.Queue()
        producer_done = asyncio.Event()
        responses: list[GenerationResponse] = []
        batch_sizes: list[int] = []

        async def producer() -> None:
            for request in requests:
                await queue.put(request)
            producer_done.set()

        async def worker() -> None:
            while True:
                try:
                    first = await asyncio.wait_for(queue.get(), timeout=0.01)
                except TimeoutError:
                    if producer_done.is_set() and queue.empty():
                        return
                    continue
                batch = [first]
                while len(batch) < self.batch_size:
                    try:
                        batch.append(queue.get_nowait())
                    except asyncio.QueueEmpty:
                        break
                result = await backend.generate(batch)
                responses.extend(result)
                batch_sizes.append(len(batch))
                for _ in batch:
                    queue.task_done()

        producer_task = asyncio.create_task(producer())
        workers = [asyncio.create_task(worker()) for _ in range(self.worker_count)]
        await producer_task
        await queue.join()
        await asyncio.gather(*workers)
        return StrategyExecution(
            responses=tuple(
                sorted(responses, key=lambda response: response.request_id)
            ),
            batch_sizes=tuple(batch_sizes),
            worker_count=self.worker_count,
            per_batch_overhead_ms=1.0,
        )


class ScalingPackTemplate(ABC):
    """Template Method para padronizar o fluxo do pack."""

    async def run(self) -> tuple[ScalingSummary, ...]:
        backend = self.build_backend()
        requests = self.build_requests()
        summaries: list[ScalingSummary] = []
        for strategy in self.strategies():
            execution = await strategy.execute(backend, requests)
            summaries.append(self.summarize(strategy.name, execution, backend))
        summaries.sort(key=lambda summary: summary.total_time_ms)
        return tuple(summaries)

    @abstractmethod
    def build_backend(self) -> MockTextGenerationBackend:
        """Constroi o backend mockado usado em todas as estrategias."""

    @abstractmethod
    def build_requests(self) -> tuple[GenerationRequest, ...]:
        """Cria a carga sintetica de requests."""

    @abstractmethod
    def strategies(self) -> tuple[ScalingStrategy, ...]:
        """Lista as estrategias comparadas."""

    def summarize(
        self,
        strategy_name: str,
        execution: StrategyExecution,
        backend: MockTextGenerationBackend,
    ) -> ScalingSummary:
        total_time_ms, average_latency_ms = _schedule_batches(
            batch_sizes=execution.batch_sizes,
            worker_count=execution.worker_count,
            backend=backend,
            per_batch_overhead_ms=execution.per_batch_overhead_ms,
        )
        processed_requests = len(execution.responses)
        return ScalingSummary(
            strategy=strategy_name,
            processed_requests=processed_requests,
            batches_processed=len(execution.batch_sizes),
            total_time_ms=total_time_ms,
            average_latency_ms=average_latency_ms,
            throughput_rps=processed_requests / (total_time_ms / 1000.0),
        )


class MockScalingPack(ScalingPackTemplate):
    """Implementa a simulacao canonica de escalabilidade."""

    def __init__(self, request_count: int = 18) -> None:
        self.request_count = request_count

    def build_backend(self) -> MockTextGenerationBackend:
        return MockTextGenerationBackend()

    def build_requests(self) -> tuple[GenerationRequest, ...]:
        return tuple(
            GenerationRequest(
                request_id=index,
                prompt=f"Summarize customer ticket {index} with SLA context.",
            )
            for index in range(1, self.request_count + 1)
        )

    def strategies(self) -> tuple[ScalingStrategy, ...]:
        return (
            AsyncDirectStrategy(),
            QueuedWorkersStrategy(),
            AsyncBatchingStrategy(),
        )


def _schedule_batches(
    batch_sizes: Sequence[int],
    worker_count: int,
    backend: MockTextGenerationBackend,
    per_batch_overhead_ms: float,
) -> tuple[float, float]:
    worker_available_at = [0.0 for _ in range(worker_count)]
    completion_times: list[float] = []
    for batch_size in batch_sizes:
        next_worker_time = min(worker_available_at)
        worker_index = worker_available_at.index(next_worker_time)
        batch_cost = backend.cost_for_batch(batch_size) + per_batch_overhead_ms
        completion_time = next_worker_time + batch_cost
        worker_available_at[worker_index] = completion_time
        completion_times.extend([completion_time] * batch_size)
    total_time_ms = max(worker_available_at, default=0.0)
    average_latency_ms = (
        sum(completion_times) / len(completion_times) if completion_times else 0.0
    )
    return total_time_ms, average_latency_ms


async def compare_scaling_strategies(
    request_count: int = 18,
) -> tuple[ScalingSummary, ...]:
    """Executa a comparacao entre estrategias de escalabilidade."""

    return await MockScalingPack(request_count=request_count).run()


def main() -> None:
    """Executa a demonstracao local com logs resumidos."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summaries = asyncio.run(compare_scaling_strategies())
    for summary in summaries:
        LOGGER.info(
            "%s -> requests=%d batches=%d total=%.1fms avg=%.1fms throughput=%.1frps",
            summary.strategy,
            summary.processed_requests,
            summary.batches_processed,
            summary.total_time_ms,
            summary.average_latency_ms,
            summary.throughput_rps,
        )


if __name__ == "__main__":
    main()
