"""Aula 01 - factory method para gerar blueprints de ambiente virtual."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from enum import StrEnum


class EnvironmentManager(StrEnum):
    """Gerenciadores suportados no demonstrador local."""

    VENV = "venv"
    VIRTUALENV = "virtualenv"


@dataclass(frozen=True, slots=True)
class BuildRequest:
    """Describe o ambiente desejado."""

    project_name: str
    python_version: str
    dependency_groups: list[str]
    platform_name: str
    manager: EnvironmentManager


@dataclass(frozen=True, slots=True)
class EnvironmentBlueprint:
    """Blueprint sem efeitos colaterais para criar e ativar o ambiente."""

    manager: str
    environment_dir: str
    create_command: str
    activate_command: str
    install_command: str
    notes: list[str]


def build_venv_blueprint(request: BuildRequest) -> EnvironmentBlueprint:
    """Factory concreta para o modulo padrão do Python."""

    activation = ".venv\\Scripts\\Activate.ps1" if request.platform_name == "windows" else "source .venv/bin/activate"
    return EnvironmentBlueprint(
        manager=request.manager.value,
        environment_dir=".venv",
        create_command="python -m venv .venv --upgrade-deps",
        activate_command=activation,
        install_command=f"python -m pip install {' '.join(request.dependency_groups)}",
        notes=[
            f"Python alvo: {request.python_version}",
            "Usa apenas componentes da biblioteca padrao.",
        ],
    )


def build_virtualenv_blueprint(request: BuildRequest) -> EnvironmentBlueprint:
    """Factory concreta para cenarios onde o time prefere virtualenv."""

    activation = ".venv\\Scripts\\activate" if request.platform_name == "windows" else "source .venv/bin/activate"
    return EnvironmentBlueprint(
        manager=request.manager.value,
        environment_dir=".venv",
        create_command=f"virtualenv .venv --python python{request.python_version}",
        activate_command=activation,
        install_command=f"python -m pip install {' '.join(request.dependency_groups)}",
        notes=[
            "Requer o pacote virtualenv instalado previamente.",
            "Costuma ser util quando ha multiplas versoes de Python no host.",
        ],
    )


def build_blueprint(request: BuildRequest) -> EnvironmentBlueprint:
    """Factory method que delega para a implementacao correta."""

    factories = {
        EnvironmentManager.VENV: build_venv_blueprint,
        EnvironmentManager.VIRTUALENV: build_virtualenv_blueprint,
    }
    return factories[request.manager](request)


def compare_blueprints() -> list[EnvironmentBlueprint]:
    """Gera um comparativo curto e local entre os dois gerenciadores."""

    base_request = {
        "project_name": "customer-retention-demo",
        "python_version": "3.11",
        "dependency_groups": ["numpy", "pandas", "scikit-learn"],
        "platform_name": "windows",
    }
    return [
        build_blueprint(BuildRequest(manager=EnvironmentManager.VENV, **base_request)),
        build_blueprint(BuildRequest(manager=EnvironmentManager.VIRTUALENV, **base_request)),
    ]


if __name__ == "__main__":
    print(json.dumps([asdict(item) for item in compare_blueprints()], indent=2, ensure_ascii=False))