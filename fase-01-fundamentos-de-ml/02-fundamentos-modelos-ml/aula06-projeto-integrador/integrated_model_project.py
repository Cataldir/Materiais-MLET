"""Projeto integrador com Builder e Facade para um fluxo end-to-end."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, field

from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42


@dataclass(frozen=True, slots=True)
class ProjectConfig:
    """Configuracao do experimento integrador."""

    dataset_name: str
    test_size: float
    random_state: int
    candidate_names: tuple[str, ...]


@dataclass(slots=True)
class ProjectConfigBuilder:
    """Builder enxuto para configurar o experimento sem espalhar parametros."""

    dataset_name: str = "breast_cancer"
    test_size: float = 0.2
    random_state: int = RANDOM_STATE
    candidate_names: list[str] = field(
        default_factory=lambda: ["logistic_regression", "random_forest", "gradient_boosting"]
    )

    def with_test_size(self, value: float) -> ProjectConfigBuilder:
        self.test_size = value
        return self

    def with_random_state(self, value: int) -> ProjectConfigBuilder:
        self.random_state = value
        return self

    def build(self) -> ProjectConfig:
        return ProjectConfig(
            dataset_name=self.dataset_name,
            test_size=self.test_size,
            random_state=self.random_state,
            candidate_names=tuple(self.candidate_names),
        )


@dataclass(frozen=True, slots=True)
class CandidateResult:
    """Resultado de um candidato avaliado."""

    name: str
    accuracy: float
    f1: float


@dataclass(frozen=True, slots=True)
class ProjectReport:
    """Saida consolidada do projeto integrador."""

    champion_name: str
    champion_accuracy: float
    candidate_results: tuple[CandidateResult, ...]
    model_card: dict[str, object]


def build_candidate_factories() -> dict[str, Callable[[int], object]]:
    """Factory local para os modelos candidatos do projeto."""

    return {
        "logistic_regression": lambda random_state: Pipeline(
            steps=[
                ("scaler", StandardScaler()),
                (
                    "model",
                    LogisticRegression(max_iter=500, random_state=random_state),
                ),
            ]
        ),
        "random_forest": lambda random_state: RandomForestClassifier(
            n_estimators=160,
            max_depth=6,
            random_state=random_state,
        ),
        "gradient_boosting": lambda random_state: GradientBoostingClassifier(
            random_state=random_state
        ),
    }


def evaluate_candidates(config: ProjectConfig) -> tuple[CandidateResult, ...]:
    """Treina e ranqueia os candidatos previstos na configuracao."""

    features, target = load_breast_cancer(return_X_y=True)
    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=config.test_size,
        random_state=config.random_state,
        stratify=target,
    )
    factories = build_candidate_factories()
    results: list[CandidateResult] = []

    for name in config.candidate_names:
        model = factories[name](config.random_state)
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)
        results.append(
            CandidateResult(
                name=name,
                accuracy=accuracy_score(y_test, predictions),
                f1=f1_score(y_test, predictions),
            )
        )

    return tuple(sorted(results, key=lambda item: (-item.accuracy, -item.f1, item.name)))


def build_model_card(config: ProjectConfig, results: tuple[CandidateResult, ...]) -> dict[str, object]:
    """Gera um model card minimo para leitura executiva."""

    champion = results[0]
    return {
        "dataset": config.dataset_name,
        "objective": "classificacao binaria para consolidar o fluxo da disciplina",
        "champion": champion.name,
        "metrics": {
            result.name: {"accuracy": result.accuracy, "f1": result.f1}
            for result in results
        },
        "recommendation": "priorizar simplicidade operacional se metricas forem proximas",
    }


def run_integrated_project(config: ProjectConfig | None = None) -> ProjectReport:
    """Facade do projeto integrador: dados, treino, ranking e model card."""

    effective_config = config or ProjectConfigBuilder().build()
    results = evaluate_candidates(effective_config)
    model_card = build_model_card(effective_config, results)
    champion = results[0]
    return ProjectReport(
        champion_name=champion.name,
        champion_accuracy=champion.accuracy,
        candidate_results=results,
        model_card=model_card,
    )


def main() -> None:
    """Executa o projeto integrador e resume a recomendacao."""

    report = run_integrated_project()
    LOGGER.info("Campeao: %s (accuracy=%.3f)", report.champion_name, report.champion_accuracy)
    for result in report.candidate_results:
        LOGGER.info("%s -> accuracy=%.3f f1=%.3f", result.name, result.accuracy, result.f1)
    LOGGER.info("Model card: %s", report.model_card)


if __name__ == "__main__":
    main()