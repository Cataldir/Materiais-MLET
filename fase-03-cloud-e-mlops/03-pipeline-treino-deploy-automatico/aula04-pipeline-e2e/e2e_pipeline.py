"""Pipeline local end-to-end com fronteiras de estagio explicitas."""

from __future__ import annotations

import logging
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)
MIN_APPROVAL_SCORE = 0.80


@dataclass(frozen=True, slots=True)
class IngestedData:
    """Representa os dados brutos apos ingestao."""

    records: int


@dataclass(frozen=True, slots=True)
class FeatureDataset:
    """Representa o conjunto pronto para treino."""

    records: int
    feature_count: int


@dataclass(frozen=True, slots=True)
class ModelPackage:
    """Representa o modelo empacotado para avaliacao e release."""

    model_name: str
    validation_score: float


@dataclass(frozen=True, slots=True)
class PipelineReport:
    """Resume a execucao ponta a ponta do pipeline."""

    stage_boundaries: tuple[str, ...]
    model_name: str
    deployed: bool
    validation_score: float


class EndToEndPipeline:
    """Executa o fluxo ponta a ponta mantendo contratos por estagio."""

    def ingest(self) -> IngestedData:
        return IngestedData(records=240)

    def build_features(self, data: IngestedData) -> FeatureDataset:
        return FeatureDataset(records=data.records, feature_count=12)

    def train(self, dataset: FeatureDataset) -> ModelPackage:
        score = 0.84 if dataset.records >= 200 else 0.76
        return ModelPackage(model_name="churn-risk-v1", validation_score=score)

    def deploy(self, package: ModelPackage) -> PipelineReport:
        deployed = package.validation_score >= MIN_APPROVAL_SCORE
        return PipelineReport(
            stage_boundaries=("ingest", "build_features", "train", "deploy"),
            model_name=package.model_name,
            deployed=deployed,
            validation_score=package.validation_score,
        )

    def run(self) -> PipelineReport:
        """Executa todo o fluxo de treino e deploy."""

        raw_data = self.ingest()
        dataset = self.build_features(raw_data)
        package = self.train(dataset)
        return self.deploy(package)


def run_demo_pipeline() -> PipelineReport:
    """Executa o pipeline canonico da aula."""

    return EndToEndPipeline().run()


def main() -> None:
    """Exibe o resultado do pipeline local."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = run_demo_pipeline()
    LOGGER.info("model=%s deployed=%s", report.model_name, report.deployed)


if __name__ == "__main__":
    main()