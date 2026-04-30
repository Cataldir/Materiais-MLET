"""Resumo local do workflow de CI usado na aula de fundamentos.

Le o workflow existente, extrai triggers, jobs e matriz de versoes e publica
um contrato local de validacao para reproducao rapida.

Uso:
    python ci_fundamentals.py
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

WORKFLOW_PATH = Path(__file__).parent / ".github" / "workflows" / "ci.yml"


@dataclass(frozen=True, slots=True)
class WorkflowStage:
    """Representa um job principal do workflow de CI."""

    job_id: str
    display_name: str
    purpose: str


@dataclass(frozen=True, slots=True)
class CIWorkflowSummary:
    """Resume o contrato do workflow para uso local e didatico."""

    workflow_name: str
    push_branches: list[str]
    pull_request_branches: list[str]
    matrix_versions: list[str]
    stages: list[WorkflowStage]
    local_commands: list[str]


def read_workflow_text(path: Path = WORKFLOW_PATH) -> str:
    """Le o workflow de CI preservado no pack."""
    return path.read_text(encoding="utf-8")


def extract_branch_lists(workflow_text: str) -> tuple[list[str], list[str]]:
    """Extrai listas de branch para push e pull request de forma leve."""
    branch_lists = re.findall(r"branches:\s*\[(.*?)\]", workflow_text)
    normalized = [
        [item.strip().strip("\"'") for item in branch_list.split(",") if item.strip()]
        for branch_list in branch_lists
    ]
    push_branches = normalized[0] if normalized else []
    pull_request_branches = normalized[1] if len(normalized) > 1 else []
    return push_branches, pull_request_branches


def extract_matrix_versions(workflow_text: str) -> list[str]:
    """Extrai a matriz de versoes Python do job de testes."""
    match = re.search(r"python-version:\s*\[(.*?)\]", workflow_text)
    if match is None:
        return []
    return [
        item.strip().strip("\"'") for item in match.group(1).split(",") if item.strip()
    ]


def build_stage_catalog(workflow_text: str) -> list[WorkflowStage]:
    """Resume os jobs principais do workflow em linguagem didatica."""
    stages: list[WorkflowStage] = []
    if re.search(r"^\s{2}lint:\s*$", workflow_text, flags=re.MULTILINE):
        stages.append(
            WorkflowStage(
                job_id="lint",
                display_name="Lint e formatacao",
                purpose="Falhar rapido quando o codigo viola estilo, tipos ou convencoes minimas.",
            )
        )
    if re.search(r"^\s{2}test:\s*$", workflow_text, flags=re.MULTILINE):
        stages.append(
            WorkflowStage(
                job_id="test",
                display_name="Testes e cobertura",
                purpose="Executar a suite nas versoes Python da matriz e publicar cobertura.",
            )
        )
    return stages


def recommended_local_commands() -> list[str]:
    """Define o contrato local minimo que espelha o workflow."""
    return [
        "ruff check .",
        "ruff format --check .",
        "pytest --cov --cov-report=xml -v",
    ]


def build_ci_lesson_summary(path: Path = WORKFLOW_PATH) -> CIWorkflowSummary:
    """Constroi o resumo didatico do workflow real preservado no pack."""
    # No GoF pattern applies; this module is a lightweight parser and contract extractor.
    workflow_text = read_workflow_text(path)
    workflow_name_match = re.search(
        r"^name:\s*(.+)$", workflow_text, flags=re.MULTILINE
    )
    workflow_name = (
        workflow_name_match.group(1).strip() if workflow_name_match else "CI"
    )
    push_branches, pull_request_branches = extract_branch_lists(workflow_text)
    matrix_versions = extract_matrix_versions(workflow_text)
    stages = build_stage_catalog(workflow_text)
    summary = CIWorkflowSummary(
        workflow_name=workflow_name,
        push_branches=push_branches,
        pull_request_branches=pull_request_branches,
        matrix_versions=matrix_versions,
        stages=stages,
        local_commands=recommended_local_commands(),
    )
    logger.info(
        "workflow=%s | jobs=%s | matrix=%s",
        summary.workflow_name,
        [stage.job_id for stage in summary.stages],
        summary.matrix_versions,
    )
    return summary


if __name__ == "__main__":
    build_ci_lesson_summary()
