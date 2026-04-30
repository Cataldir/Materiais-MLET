"""Factory Method para gerar manifestos de dependencias em multiplos formatos."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DependencyProfile:
    """Perfil de dependencias do projeto de ML."""

    project_name: str
    version: str
    core_dependencies: tuple[str, ...]
    dev_dependencies: tuple[str, ...]
    environment_variables: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class EnvironmentManifest:
    """Manifesto materializado para uma ferramenta especifica."""

    tool: str
    files: dict[str, str]


class ManifestFactory:
    """Factory base para gerar artefatos de ambiente."""

    tool_name = "base"

    def create_manifest(self, profile: DependencyProfile) -> EnvironmentManifest:
        raise NotImplementedError


class VenvManifestFactory(ManifestFactory):
    tool_name = "venv"

    def create_manifest(self, profile: DependencyProfile) -> EnvironmentManifest:
        requirements = "\n".join(profile.core_dependencies + profile.dev_dependencies)
        env_example = "\n".join(f"{name}=change-me" for name in profile.environment_variables)
        return EnvironmentManifest(
            tool=self.tool_name,
            files={
                "requirements.txt": requirements,
                ".env.example": env_example,
                "README_ENV.md": "python -m venv .venv\npip install -r requirements.txt",
            },
        )


class PoetryManifestFactory(ManifestFactory):
    tool_name = "poetry"

    def create_manifest(self, profile: DependencyProfile) -> EnvironmentManifest:
        main_block = "\n".join(
            f'{dependency.split("==")[0]} = "^{dependency.split("==")[1]}"'
            for dependency in profile.core_dependencies
        )
        dev_block = "\n".join(
            f'{dependency.split("==")[0]} = "^{dependency.split("==")[1]}"'
            for dependency in profile.dev_dependencies
        )
        pyproject = (
            "[tool.poetry]\n"
            f'name = "{profile.project_name}"\n'
            f'version = "{profile.version}"\n\n'
            "[tool.poetry.dependencies]\npython = \"^3.12\"\n"
            f"{main_block}\n\n"
            "[tool.poetry.group.dev.dependencies]\n"
            f"{dev_block}\n"
        )
        return EnvironmentManifest(tool=self.tool_name, files={"pyproject.toml": pyproject})


class UvManifestFactory(ManifestFactory):
    tool_name = "uv"

    def create_manifest(self, profile: DependencyProfile) -> EnvironmentManifest:
        dependencies = ",\n    ".join(f'"{dependency}"' for dependency in profile.core_dependencies)
        optional = ",\n    ".join(f'"{dependency}"' for dependency in profile.dev_dependencies)
        pyproject = (
            "[project]\n"
            f'name = "{profile.project_name}"\n'
            f'version = "{profile.version}"\n'
            "requires-python = \">=3.12\"\n"
            "dependencies = [\n    "
            f"{dependencies}\n]\n\n"
            "[project.optional-dependencies]\n"
            "dev = [\n    "
            f"{optional}\n]\n"
        )
        return EnvironmentManifest(
            tool=self.tool_name,
            files={
                "pyproject.toml": pyproject,
                "uv.md": "uv sync\nuv run python -m pytest",
            },
        )


def build_demo_profile() -> DependencyProfile:
    """Constroi um perfil de dependencias pequeno e realista."""

    return DependencyProfile(
        project_name="mlet-dependency-demo",
        version="0.1.0",
        core_dependencies=("scikit-learn==1.7.0", "pydantic==2.11.0"),
        dev_dependencies=("pytest==8.3.0", "ruff==0.11.0"),
        environment_variables=("APP_ENV", "MODEL_PATH"),
    )


def build_manifests(profile: DependencyProfile | None = None) -> tuple[EnvironmentManifest, ...]:
    """Gera manifestos equivalentes usando tres ferramentas diferentes."""

    effective_profile = profile or build_demo_profile()
    factories: tuple[ManifestFactory, ...] = (
        VenvManifestFactory(),
        PoetryManifestFactory(),
        UvManifestFactory(),
    )
    return tuple(factory.create_manifest(effective_profile) for factory in factories)


def main() -> None:
    """Imprime os arquivos gerados por cada ferramenta."""

    for manifest in build_manifests():
        LOGGER.info("Ferramenta: %s", manifest.tool)
        for file_name in sorted(manifest.files):
            LOGGER.info("- %s", file_name)


if __name__ == "__main__":
    main()