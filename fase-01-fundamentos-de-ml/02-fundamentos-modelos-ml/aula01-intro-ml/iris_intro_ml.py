"""Intro ML com o dataset Iris.

Pack canonico derivado de `origin/fundamentos-python`, normalizado para
execucao local sem celulas de instalacao e com funcoes reutilizaveis.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True)
class IrisRunSummary:
    """Resumo da execucao do baseline de classificacao."""

    accuracy: float
    confusion_matrix: list[list[int]]
    classes: tuple[str, ...]
    report: dict[str, dict[str, float] | float]


def load_iris_frame() -> pd.DataFrame:
    """Carrega o dataset Iris em um DataFrame com a coluna de especie."""
    dataset = load_iris(as_frame=True)
    frame = dataset.frame.copy()
    target_names = dict(enumerate(dataset.target_names))
    frame["species"] = frame["target"].map(target_names)
    return frame


def train_iris_baseline(
    test_size: float = 0.2,
    random_state: int = 42,
) -> IrisRunSummary:
    """Treina um baseline simples de classificacao para o Iris."""
    frame = load_iris_frame()
    features = frame.drop(columns=["target", "species"])
    target = frame["target"]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=test_size,
        random_state=random_state,
        stratify=target,
    )

    pipeline = Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            (
                "classifier",
                LogisticRegression(max_iter=300, multi_class="auto", random_state=random_state),
            ),
        ]
    )
    pipeline.fit(x_train, y_train)
    predictions = pipeline.predict(x_test)

    summary = IrisRunSummary(
        accuracy=accuracy_score(y_test, predictions),
        confusion_matrix=confusion_matrix(y_test, predictions).tolist(),
        classes=tuple(load_iris().target_names),
        report=classification_report(y_test, predictions, output_dict=True),
    )
    LOGGER.info("Acuracia do baseline Iris: %.3f", summary.accuracy)
    LOGGER.info("Matriz de confusao: %s", summary.confusion_matrix)
    return summary


def main() -> None:
    """Executa o baseline e registra um resumo em log."""
    summary = train_iris_baseline()
    for class_name in summary.classes:
        metrics = summary.report[class_name]
        LOGGER.info(
            "Classe %s -> precision=%.3f recall=%.3f f1=%.3f",
            class_name,
            metrics["precision"],
            metrics["recall"],
            metrics["f1-score"],
        )


if __name__ == "__main__":
    main()