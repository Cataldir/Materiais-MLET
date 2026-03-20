"""Aula 03 - Strategy para comparar Poetry e uv."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class DemoProject:
    """Projeto minimo compartilhado pelas estrategias."""

    name: str
    python_constraint: str
    dependencies: list[str]


@dataclass(frozen=True, slots=True)
class ToolSummary:
    """Resumo do fluxo operacional de uma ferramenta."""

    tool: str
    lockfile: str
    create_command: str
    add_dependency_command: str
    sync_command: str
    sample_project_file: str


class DependencyStrategy(Protocol):
    """Contrato comum para as estrategias."""

    tool: str
    lockfile: str

    def summarize(self, project: DemoProject, root_dir: Path) -> ToolSummary:
        """Resume o uso da estrategia para um projeto."""


class PoetryStrategy:
    tool = "poetry"
    lockfile = "poetry.lock"

    def summarize(self, project: DemoProject, root_dir: Path) -> ToolSummary:
        project_file = root_dir / "poetry_project" / "pyproject.toml"
        return ToolSummary(
            tool=self.tool,
            lockfile=self.lockfile,
            create_command=f"poetry init --name {project.name}",
            add_dependency_command="poetry add pandas scikit-learn numpy",
            sync_command="poetry install --sync",
            sample_project_file=str(project_file.relative_to(root_dir)),
        )


class UvStrategy:
    tool = "uv"
    lockfile = "uv.lock"

    def summarize(self, project: DemoProject, root_dir: Path) -> ToolSummary:
        project_file = root_dir / "uv_project" / "pyproject.toml"
        return ToolSummary(
            tool=self.tool,
            lockfile=self.lockfile,
            create_command=f"uv init {project.name}",
            add_dependency_command="uv add pandas scikit-learn numpy",
            sync_command="uv sync --frozen",
            sample_project_file=project_file.relative_to(root_dir).as_posix(),
        )


def build_project() -> DemoProject:
    """Constroi o projeto base usado na comparacao."""

    return DemoProject(
        name="feature-store-demo",
        python_constraint=">=3.11",
        dependencies=["numpy>=1.26", "pandas>=2.2", "scikit-learn>=1.4"],
    )


def compare_tools(root_dir: Path | None = None) -> list[ToolSummary]:
    """Aplica as duas estrategias ao mesmo projeto."""

    base_dir = root_dir or Path(__file__).resolve().parent
    project = build_project()
    strategies: list[DependencyStrategy] = [PoetryStrategy(), UvStrategy()]
    return [strategy.summarize(project, base_dir) for strategy in strategies]


if __name__ == "__main__":
    print(json.dumps([asdict(item) for item in compare_tools()], indent=2, ensure_ascii=False))