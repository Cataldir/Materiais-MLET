"""Pipeline local de CI/CD implementado como pipes-and-filters."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PipelineArtifact:
    """Representa o artefato enriquecido por cada filtro."""

    changed_files: tuple[str, ...]
    quality_checks: tuple[str, ...] = ()
    packaged_version: str | None = None
    release_channel: str | None = None


@dataclass(frozen=True, slots=True)
class StageReport:
    """Resume o efeito de cada etapa do pipeline."""

    name: str
    status: str


@dataclass(frozen=True, slots=True)
class PipelineRun:
    """Estado final e trilha de auditoria do pipeline."""

    artifact: PipelineArtifact
    reports: tuple[StageReport, ...]


class PipelineFilter(Protocol):
    """Contrato dos filtros aplicados ao artefato."""

    name: str

    def apply(self, artifact: PipelineArtifact) -> PipelineArtifact:
        """Transforma o artefato de entrada em um novo artefato."""


class LintFilter:
    """Valida convencoes minimas antes de continuar."""

    name = "lint"

    def apply(self, artifact: PipelineArtifact) -> PipelineArtifact:
        return PipelineArtifact(
            changed_files=artifact.changed_files,
            quality_checks=artifact.quality_checks + ("ruff",),
            packaged_version=artifact.packaged_version,
            release_channel=artifact.release_channel,
        )


class TestFilter:
    """Registra a aprovacao dos testes automatizados."""

    name = "tests"

    def apply(self, artifact: PipelineArtifact) -> PipelineArtifact:
        return PipelineArtifact(
            changed_files=artifact.changed_files,
            quality_checks=artifact.quality_checks + ("pytest",),
            packaged_version=artifact.packaged_version,
            release_channel=artifact.release_channel,
        )


class PackageFilter:
    """Define a versao do pacote que sera promovido."""

    name = "package"

    def __init__(self, version: str) -> None:
        self.version = version

    def apply(self, artifact: PipelineArtifact) -> PipelineArtifact:
        return PipelineArtifact(
            changed_files=artifact.changed_files,
            quality_checks=artifact.quality_checks,
            packaged_version=f"release-{self.version}",
            release_channel=artifact.release_channel,
        )


class ReleaseFilter:
    """Marca o canal de entrega final do artefato."""

    name = "release"

    def __init__(self, channel: str) -> None:
        self.channel = channel

    def apply(self, artifact: PipelineArtifact) -> PipelineArtifact:
        return PipelineArtifact(
            changed_files=artifact.changed_files,
            quality_checks=artifact.quality_checks,
            packaged_version=artifact.packaged_version,
            release_channel=self.channel,
        )


def run_local_pipeline(version: str = "v1.4.0") -> PipelineRun:
    """Executa o pipeline local completo com filtros deterministas."""

    artifact = PipelineArtifact(
        changed_files=(
            "src/api.py",
            "src/model.py",
            "tests/test_api.py",
        )
    )
    filters: tuple[PipelineFilter, ...] = (
        LintFilter(),
        TestFilter(),
        PackageFilter(version=version),
        ReleaseFilter(channel="staging"),
    )
    reports: list[StageReport] = []
    for pipeline_filter in filters:
        artifact = pipeline_filter.apply(artifact)
        reports.append(StageReport(name=pipeline_filter.name, status="passed"))
    return PipelineRun(artifact=artifact, reports=tuple(reports))


def main() -> None:
    """Executa o pipeline local e imprime o resumo."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    run = run_local_pipeline()
    LOGGER.info(
        "stages=%s version=%s channel=%s",
        [report.name for report in run.reports],
        run.artifact.packaged_version,
        run.artifact.release_channel,
    )


if __name__ == "__main__":
    main()