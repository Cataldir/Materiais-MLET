"""Aula 07 - command pipeline para CI local de DVC e tracking."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class StageResult:
    """Resultado de uma etapa do pipeline."""

    name: str
    command: str
    status: str
    evidence: str


class PipelineCommand(Protocol):
    """Contrato comum para comandos da pipeline."""

    name: str

    def run(self, root_dir: Path) -> StageResult:
        """Executa a etapa em modo determinista."""


class ValidatePackCommand:
    name = "validate-pack"

    def run(self, root_dir: Path) -> StageResult:
        integrated_dir = root_dir.parent / "aula06-pipeline-integrado"
        required = [
            integrated_dir / "dvc.yaml",
            integrated_dir / "params.yaml",
            integrated_dir / "pipeline_facade.py",
        ]
        status = "ok" if all(path.exists() for path in required) else "fail"
        return StageResult(
            name=self.name,
            command="python -m pytest tests/test_first_wave_extraction.py -k phase02",
            status=status,
            evidence="pipeline_contracts_present",
        )


class DryRunPipelineCommand:
    name = "dry-run-pipeline"

    def run(self, root_dir: Path) -> StageResult:
        return StageResult(
            name=self.name,
            command="python ../aula06-pipeline-integrado/pipeline_facade.py",
            status="ok",
            evidence="local_pipeline_plan_rendered",
        )


class PublishMetricsCommand:
    name = "publish-metrics"

    def run(self, root_dir: Path) -> StageResult:
        workflow_file = root_dir / ".github" / "workflows" / "dvc_mlflow_ci.yml"
        status = "ok" if workflow_file.exists() else "fail"
        return StageResult(
            name=self.name,
            command="python -c \"print('upload metrics artifact')\"",
            status=status,
            evidence="metrics_and_tracking_artifacts",
        )


def build_ci_plan() -> list[StageResult]:
    """Monta a pipeline local em ordem fixa."""

    root_dir = Path(__file__).resolve().parent
    commands: list[PipelineCommand] = [
        ValidatePackCommand(),
        DryRunPipelineCommand(),
        PublishMetricsCommand(),
    ]
    return [command.run(root_dir) for command in commands]


if __name__ == "__main__":
    print(json.dumps([asdict(item) for item in build_ci_plan()], indent=2, ensure_ascii=False))