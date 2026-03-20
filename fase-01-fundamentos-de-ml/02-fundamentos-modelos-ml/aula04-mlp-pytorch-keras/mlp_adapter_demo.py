"""Comparacao de backends MLP usando Strategy e Adapter sobre sklearn."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass

from sklearn.datasets import load_wine
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42


@dataclass(frozen=True, slots=True)
class BackendAdapter:
    """Representa uma estrategia de treino adaptada a um contrato comum."""

    name: str
    builder: Callable[[int], object]


@dataclass(frozen=True, slots=True)
class ModelRunSummary:
    """Resumo de desempenho para um backend avaliado."""

    backend: str
    accuracy: float
    train_size: int
    test_size: int


def build_pytorch_style_backend(random_state: int) -> Pipeline:
    """Monta um MLP denso com configuracao inspirada em PyTorch."""

    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                MLPClassifier(
                    hidden_layer_sizes=(64, 32),
                    activation="relu",
                    solver="adam",
                    max_iter=700,
                    early_stopping=True,
                    random_state=random_state,
                ),
            ),
        ]
    )


def build_keras_style_backend(random_state: int) -> Pipeline:
    """Monta um MLP com regularizacao mais forte, inspirada em Keras."""

    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "model",
                MLPClassifier(
                    hidden_layer_sizes=(128,),
                    activation="relu",
                    alpha=0.01,
                    batch_size=16,
                    max_iter=700,
                    early_stopping=True,
                    random_state=random_state,
                ),
            ),
        ]
    )


def build_xgboost_style_backend(random_state: int) -> GradientBoostingClassifier:
    """Entrega um baseline tree-based com API equivalente ao fluxo das MLPs."""

    return GradientBoostingClassifier(random_state=random_state)


def evaluate_adapter(adapter: BackendAdapter, random_state: int = RANDOM_STATE) -> ModelRunSummary:
    """Treina e avalia uma estrategia adaptada no dataset Wine."""

    features, target = load_wine(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.25,
        random_state=random_state,
        stratify=target,
    )
    model = adapter.builder(random_state)
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    return ModelRunSummary(
        backend=adapter.name,
        accuracy=accuracy_score(y_test, predictions),
        train_size=len(x_train),
        test_size=len(x_test),
    )


def compare_backends(random_state: int = RANDOM_STATE) -> list[ModelRunSummary]:
    """Compara tres estrategias sob o mesmo contrato de avaliacao."""

    adapters = [
        BackendAdapter("pytorch_style_mlp", build_pytorch_style_backend),
        BackendAdapter("keras_style_mlp", build_keras_style_backend),
        BackendAdapter("xgboost_style_baseline", build_xgboost_style_backend),
    ]
    summaries = [evaluate_adapter(adapter, random_state=random_state) for adapter in adapters]
    return sorted(summaries, key=lambda item: (-item.accuracy, item.backend))


def main() -> None:
    """Executa a comparacao e imprime um ranking simples."""

    for summary in compare_backends():
        LOGGER.info(
            "%s -> accuracy=%.3f (train=%d test=%d)",
            summary.backend,
            summary.accuracy,
            summary.train_size,
            summary.test_size,
        )


if __name__ == "__main__":
    main()