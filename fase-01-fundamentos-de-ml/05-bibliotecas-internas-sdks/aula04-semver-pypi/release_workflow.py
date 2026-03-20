"""Template Method e State para um pipeline de release interno."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


class ReleaseState(StrEnum):
    """Estados do ciclo de release."""

    DRAFT = "draft"
    VALIDATED = "validated"
    PACKAGED = "packaged"
    PUBLISHED = "published"


@dataclass(frozen=True, slots=True)
class ReleaseRequest:
    """Dados necessarios para gerar uma release."""

    current_version: str
    change_type: str
    release_notes: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class ReleaseOutcome:
    """Resultado do pipeline de release."""

    next_version: str
    final_state: ReleaseState
    state_history: tuple[ReleaseState, ...]
    artifacts: dict[str, str]


def bump_semver(version: str, change_type: str) -> str:
    """Aplica uma regra simples de SemVer."""

    major, minor, patch = (int(part) for part in version.split("."))
    if change_type == "major":
        return f"{major + 1}.0.0"
    if change_type == "minor":
        return f"{major}.{minor + 1}.0"
    if change_type == "patch":
        return f"{major}.{minor}.{patch + 1}"
    raise ValueError(f"change_type invalido: {change_type}")


class ReleaseTemplate:
    """Template Method do fluxo de validacao ate publicacao."""

    def run(self, request: ReleaseRequest) -> ReleaseOutcome:
        state_history = [ReleaseState.DRAFT]
        self.validate_request(request)
        state_history.append(ReleaseState.VALIDATED)
        next_version = bump_semver(request.current_version, request.change_type)
        artifacts = self.build_artifacts(request, next_version)
        state_history.append(ReleaseState.PACKAGED)
        self.publish(next_version, artifacts)
        state_history.append(ReleaseState.PUBLISHED)
        return ReleaseOutcome(
            next_version=next_version,
            final_state=ReleaseState.PUBLISHED,
            state_history=tuple(state_history),
            artifacts=artifacts,
        )

    def validate_request(self, request: ReleaseRequest) -> None:
        if request.change_type not in {"major", "minor", "patch"}:
            raise ValueError("change_type deve ser major, minor ou patch")
        if not request.release_notes:
            raise ValueError("release_notes nao pode ser vazio")

    def build_artifacts(self, request: ReleaseRequest, next_version: str) -> dict[str, str]:
        changelog = "\n".join(
            [
                f"## {next_version}",
                *[f"- {note}" for note in request.release_notes],
            ]
        )
        pyproject = "\n".join(
            [
                "[project]",
                'name = "ml-utils"',
                f'version = "{next_version}"',
                'requires-python = ">=3.12"',
            ]
        )
        return {"CHANGELOG.md": changelog, "pyproject.toml": pyproject}

    def publish(self, next_version: str, artifacts: dict[str, str]) -> None:
        raise NotImplementedError


class InternalRegistryRelease(ReleaseTemplate):
    """Especializacao que simula publicacao em indice interno."""

    def publish(self, next_version: str, artifacts: dict[str, str]) -> None:
        LOGGER.info(
            "Publicando %s com artefatos %s no indice interno",
            next_version,
            sorted(artifacts),
        )


def run_release_demo(
    current_version: str = "1.4.2",
    change_type: str = "minor",
) -> ReleaseOutcome:
    """Executa um release de exemplo com notes curtas."""

    request = ReleaseRequest(
        current_version=current_version,
        change_type=change_type,
        release_notes=(
            "adiciona facade de tracking para sklearn",
            "padroniza documentacao do pacote interno",
        ),
    )
    return InternalRegistryRelease().run(request)


def main() -> None:
    """Executa o fluxo de release e imprime o resultado."""

    outcome = run_release_demo()
    LOGGER.info("Proxima versao: %s", outcome.next_version)
    LOGGER.info("Historico: %s", outcome.state_history)


if __name__ == "__main__":
    main()