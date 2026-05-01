"""Modelo local de DAG para explicar conceitos basicos de pipeline."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from graphlib import TopologicalSorter

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class StageMetadata:
    """Define os metadados minimos de um estagio do pipeline."""

    name: str
    owner: str
    depends_on: tuple[str, ...]
    output: str


@dataclass(frozen=True, slots=True)
class PipelineBlueprint:
    """Agrupa catalogo e ordem valida do pipeline."""

    stages: tuple[StageMetadata, ...]
    execution_order: tuple[str, ...]


def build_reference_pipeline() -> PipelineBlueprint:
    """Constroi um pipeline canonico e devolve sua ordem topologica."""

    # No GoF pattern applies; this module is a simple metadata model for a DAG.
    stages = (
        StageMetadata("extract", "data-platform", (), "raw_dataset.parquet"),
        StageMetadata(
            "validate",
            "data-quality",
            ("extract",),
            "validation_report.json",
        ),
        StageMetadata("train", "ml-engineering", ("validate",), "model.pkl"),
        StageMetadata(
            "package",
            "ml-platform",
            ("train",),
            "model_bundle.tar.gz",
        ),
        StageMetadata("deploy", "ml-platform", ("package",), "release_manifest.json"),
    )
    sorter = TopologicalSorter(
        {stage.name: stage.depends_on for stage in stages}
    )
    execution_order = tuple(sorter.static_order())
    return PipelineBlueprint(stages=stages, execution_order=execution_order)


def main() -> None:
    """Imprime a ordem de execucao do DAG local."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    blueprint = build_reference_pipeline()
    LOGGER.info("order=%s", list(blueprint.execution_order))


if __name__ == "__main__":
    main()