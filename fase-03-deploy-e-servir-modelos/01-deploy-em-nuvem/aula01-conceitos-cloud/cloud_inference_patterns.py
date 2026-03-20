"""Compara padroes de inferencia cloud sobre o mesmo modelo sklearn.

O pack usa apenas o dataset publico Breast Cancer do scikit-learn e aplica o
mesmo pipeline de classificacao em tres estrategias de invocacao: batch,
realtime API e serverless-style.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)
REQUEST_SAMPLE_SIZE = 24
RANDOM_STATE = 42


@dataclass(frozen=True)
class InferenceRequest:
    """Representa uma requisicao de inferencia local."""

    request_id: int
    features: tuple[float, ...]
    expected_label: int


@dataclass(frozen=True)
class ModelArtifacts:
    """Agrupa pipeline treinado e requests de avaliacao."""

    pipeline: Pipeline
    requests: tuple[InferenceRequest, ...]


@dataclass(frozen=True)
class StrategyExecution:
    """Resultado bruto de uma estrategia antes do resumo final."""

    predictions: tuple[int, ...]
    total_latency_ms: float


@dataclass(frozen=True)
class InvocationSummary:
    """Resumo comparativo de uma estrategia de inferencia."""

    mode: str
    accuracy: float
    correct_predictions: int
    total_latency_ms: float
    average_latency_ms: float
    throughput_rps: float


class InvocationStrategy(Protocol):
    """Contrato para estrategias de invocacao intercambiaveis."""

    name: str

    def execute(
        self, pipeline: Pipeline, requests: Sequence[InferenceRequest]
    ) -> StrategyExecution:
        """Executa inferencia e retorna previsoes com custo modelado."""


class BatchInvocationStrategy:
    """Executa varias observacoes em uma chamada unica."""

    name = "batch"

    def execute(
        self, pipeline: Pipeline, requests: Sequence[InferenceRequest]
    ) -> StrategyExecution:
        feature_matrix = np.asarray(
            [request.features for request in requests], dtype=float
        )
        predictions = tuple(
            int(prediction) for prediction in pipeline.predict(feature_matrix)
        )
        total_latency_ms = 8.0 + 0.35 * len(requests)
        return StrategyExecution(
            predictions=predictions, total_latency_ms=total_latency_ms
        )


class RealtimeAPIInvocationStrategy:
    """Simula uma API que atende uma requisicao por chamada."""

    name = "realtime_api"

    def execute(
        self, pipeline: Pipeline, requests: Sequence[InferenceRequest]
    ) -> StrategyExecution:
        predictions: list[int] = []
        for request in requests:
            feature_matrix = np.asarray([request.features], dtype=float)
            predictions.append(int(pipeline.predict(feature_matrix)[0]))
        total_latency_ms = len(requests) * 6.5
        return StrategyExecution(
            predictions=tuple(predictions), total_latency_ms=total_latency_ms
        )


class ServerlessInvocationStrategy:
    """Simula invocacoes serverless com cold starts recorrentes."""

    name = "serverless"

    def __init__(self, cold_start_every: int = 6, cold_start_ms: float = 75.0) -> None:
        self.cold_start_every = cold_start_every
        self.cold_start_ms = cold_start_ms

    def execute(
        self, pipeline: Pipeline, requests: Sequence[InferenceRequest]
    ) -> StrategyExecution:
        predictions: list[int] = []
        cold_starts = 0
        for index, request in enumerate(requests, start=1):
            feature_matrix = np.asarray([request.features], dtype=float)
            predictions.append(int(pipeline.predict(feature_matrix)[0]))
            if index == 1 or (index - 1) % self.cold_start_every == 0:
                cold_starts += 1
        total_latency_ms = len(requests) * 8.0 + cold_starts * self.cold_start_ms
        return StrategyExecution(
            predictions=tuple(predictions), total_latency_ms=total_latency_ms
        )


class CloudComparisonTemplate(ABC):
    """Template Method para manter o fluxo do pack estavel."""

    def run(self) -> tuple[InvocationSummary, ...]:
        artifacts = self.prepare_artifacts()
        summaries = [
            self.evaluate_strategy(strategy, artifacts)
            for strategy in self.strategies()
        ]
        summaries.sort(key=lambda summary: summary.total_latency_ms)
        return tuple(summaries)

    @abstractmethod
    def prepare_artifacts(self) -> ModelArtifacts:
        """Treina o modelo e prepara requests de avaliacao."""

    @abstractmethod
    def strategies(self) -> tuple[InvocationStrategy, ...]:
        """Retorna as estrategias a serem comparadas."""

    def evaluate_strategy(
        self,
        strategy: InvocationStrategy,
        artifacts: ModelArtifacts,
    ) -> InvocationSummary:
        execution = strategy.execute(artifacts.pipeline, artifacts.requests)
        expected = [request.expected_label for request in artifacts.requests]
        accuracy = accuracy_score(expected, execution.predictions)
        total_latency_ms = execution.total_latency_ms
        return InvocationSummary(
            mode=strategy.name,
            accuracy=float(accuracy),
            correct_predictions=sum(
                int(prediction == request.expected_label)
                for prediction, request in zip(
                    execution.predictions, artifacts.requests, strict=True
                )
            ),
            total_latency_ms=total_latency_ms,
            average_latency_ms=total_latency_ms / len(artifacts.requests),
            throughput_rps=len(artifacts.requests) / (total_latency_ms / 1000.0),
        )


class SklearnCloudComparisonPack(CloudComparisonTemplate):
    """Implementa o fluxo canonico para comparar padroes de deploy."""

    def prepare_artifacts(self) -> ModelArtifacts:
        dataset = load_breast_cancer()
        features_train, features_test, target_train, target_test = train_test_split(
            dataset.data,
            dataset.target,
            test_size=0.25,
            stratify=dataset.target,
            random_state=RANDOM_STATE,
        )
        pipeline = Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "classifier",
                    LogisticRegression(max_iter=400, random_state=RANDOM_STATE),
                ),
            ]
        )
        pipeline.fit(features_train, target_train)

        requests = tuple(
            InferenceRequest(
                request_id=index,
                features=tuple(float(value) for value in row),
                expected_label=int(label),
            )
            for index, (row, label) in enumerate(
                zip(
                    features_test[:REQUEST_SAMPLE_SIZE],
                    target_test[:REQUEST_SAMPLE_SIZE],
                    strict=True,
                ),
                start=1,
            )
        )
        return ModelArtifacts(pipeline=pipeline, requests=requests)

    def strategies(self) -> tuple[InvocationStrategy, ...]:
        return (
            BatchInvocationStrategy(),
            RealtimeAPIInvocationStrategy(),
            ServerlessInvocationStrategy(),
        )


def compare_invocation_modes() -> tuple[InvocationSummary, ...]:
    """Executa o comparativo entre batch, realtime e serverless."""

    return SklearnCloudComparisonPack().run()


def main() -> None:
    """Executa o pack com logs resumidos."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summaries = compare_invocation_modes()
    for summary in summaries:
        LOGGER.info(
            "%s -> accuracy=%.3f latency_total=%.1fms latency_media=%.1fms throughput=%.1frps",
            summary.mode,
            summary.accuracy,
            summary.total_latency_ms,
            summary.average_latency_ms,
            summary.throughput_rps,
        )


if __name__ == "__main__":
    main()
