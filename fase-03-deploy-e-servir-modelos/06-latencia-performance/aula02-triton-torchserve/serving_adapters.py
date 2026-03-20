"""Comparativo local entre adapters inspirados em Triton e TorchServe."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class InferencePayload:
    """Payload compartilhado pelos dois adapters."""

    model_name: str
    batch_size: int
    tensor_shape: tuple[int, ...]


@dataclass(frozen=True, slots=True)
class ServingReport:
    """Resumo comparavel do serving backend."""

    backend: str
    packaged_artifact: str
    throughput_rps: float
    average_latency_ms: float


class ServingAdapter(Protocol):
    """Contrato dos backends comparados na aula."""

    backend_name: str

    def serve(self, payload: InferencePayload) -> ServingReport:
        """Retorna um resumo deterministico de serving."""


class TritonServingAdapter:
    """Adapter orientado a batching dinamico e throughput."""

    backend_name = "triton"

    def serve(self, payload: InferencePayload) -> ServingReport:
        return ServingReport(
            backend=self.backend_name,
            packaged_artifact=f"{payload.model_name}/config.pbtxt",
            throughput_rps=420.0,
            average_latency_ms=18.0,
        )


class TorchServeAdapter:
    """Adapter orientado a handler Python e model archive."""

    backend_name = "torchserve"

    def serve(self, payload: InferencePayload) -> ServingReport:
        return ServingReport(
            backend=self.backend_name,
            packaged_artifact=f"{payload.model_name}.mar",
            throughput_rps=310.0,
            average_latency_ms=24.0,
        )


def compare_serving_backends() -> tuple[ServingReport, ...]:
    """Executa o comparativo local entre os dois backends."""

    payload = InferencePayload("vision-model", batch_size=8, tensor_shape=(8, 3, 224, 224))
    adapters: tuple[ServingAdapter, ...] = (
        TritonServingAdapter(),
        TorchServeAdapter(),
    )
    return tuple(adapter.serve(payload) for adapter in adapters)


def main() -> None:
    """Imprime o resumo do comparativo de serving."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for report in compare_serving_backends():
        LOGGER.info("%s -> %.1frps", report.backend, report.throughput_rps)


if __name__ == "__main__":
    main()