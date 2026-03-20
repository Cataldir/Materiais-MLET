"""Workflow de Git modelado com Command para estudo local."""

from __future__ import annotations

import logging
from collections.abc import Callable
from dataclasses import dataclass, replace

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class RepoState:
    """Estado simplificado de um repositorio durante o workflow."""

    branch: str
    staged_files: tuple[str, ...]
    history: tuple[str, ...]
    tests_green: bool
    review_requested: bool
    approved: bool
    merged: bool


@dataclass(frozen=True, slots=True)
class WorkflowCommand:
    """Representa um comando que transforma o estado do repositorio."""

    name: str
    executor: Callable[[RepoState], RepoState]

    def run(self, state: RepoState) -> RepoState:
        return self.executor(state)


def checkout_feature_branch(branch_name: str) -> WorkflowCommand:
    return WorkflowCommand(
        name=f"checkout:{branch_name}",
        executor=lambda state: replace(
            state,
            branch=branch_name,
            history=state.history + (f"checkout:{branch_name}",),
        ),
    )


def stage_files(files: tuple[str, ...]) -> WorkflowCommand:
    return WorkflowCommand(
        name="stage",
        executor=lambda state: replace(
            state,
            staged_files=files,
            history=state.history + (f"stage:{','.join(files)}",),
        ),
    )


def run_tests() -> WorkflowCommand:
    return WorkflowCommand(
        name="test",
        executor=lambda state: replace(
            state,
            tests_green=True,
            history=state.history + ("test:green",),
        ),
    )


def commit_changes(message: str) -> WorkflowCommand:
    return WorkflowCommand(
        name="commit",
        executor=lambda state: replace(
            state,
            history=state.history + (f"commit:{message}",),
        ),
    )


def open_pull_request() -> WorkflowCommand:
    return WorkflowCommand(
        name="open_pr",
        executor=lambda state: replace(
            state,
            review_requested=True,
            history=state.history + ("pull_request:opened",),
        ),
    )


def approve_pull_request() -> WorkflowCommand:
    return WorkflowCommand(
        name="approve_pr",
        executor=lambda state: replace(
            state,
            approved=True,
            history=state.history + ("pull_request:approved",),
        ),
    )


def merge_pull_request() -> WorkflowCommand:
    def executor(state: RepoState) -> RepoState:
        if not state.tests_green or not state.review_requested or not state.approved:
            raise ValueError("PR nao esta pronta para merge")
        return replace(
            state,
            branch="main",
            merged=True,
            history=state.history + ("merge:main",),
        )

    return WorkflowCommand(name="merge_pr", executor=executor)


def build_default_workflow(changed_files: tuple[str, ...]) -> tuple[WorkflowCommand, ...]:
    """Monta o fluxo padrao de colaboracao para um pack de ML."""

    return (
        checkout_feature_branch("feature/aula-git-workflow"),
        stage_files(changed_files),
        run_tests(),
        commit_changes("feat: adiciona material da aula de git workflow"),
        open_pull_request(),
        approve_pull_request(),
        merge_pull_request(),
    )


def run_git_workflow_demo(
    changed_files: tuple[str, ...] = ("git_workflow_demo.py", "README.md"),
) -> RepoState:
    """Executa o workflow completo em memoria."""

    state = RepoState(
        branch="main",
        staged_files=(),
        history=(),
        tests_green=False,
        review_requested=False,
        approved=False,
        merged=False,
    )
    for command in build_default_workflow(changed_files):
        state = command.run(state)
    return state


def main() -> None:
    """Executa o exemplo e imprime o historico de comandos."""

    final_state = run_git_workflow_demo()
    for item in final_state.history:
        LOGGER.info(item)
    LOGGER.info("Branch final: %s | merged=%s", final_state.branch, final_state.merged)


if __name__ == "__main__":
    main()