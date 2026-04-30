"""Aula 03 - adapter para remotos DVC com fallback offline."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Protocol


@dataclass(frozen=True, slots=True)
class RemoteDefinition:
    """Define um remoto desejado para a demo."""

    name: str
    uri: str


@dataclass(frozen=True, slots=True)
class RemotePlan:
    """Plano final de configuracao para o remoto."""

    name: str
    backend: str
    uri: str
    requires_credentials: bool
    fallback_uri: str
    setup_commands: list[str]


class RemoteAdapter(Protocol):
    """Contrato comum entre backends."""

    backend: str

    def build_plan(self, remote: RemoteDefinition, base_dir: Path) -> RemotePlan:
        """Produz um plano local-first para o backend."""


class LocalAdapter:
    backend = "local"

    def build_plan(self, remote: RemoteDefinition, base_dir: Path) -> RemotePlan:
        fallback_dir = base_dir / ".demo-remotes" / remote.name
        return RemotePlan(
            name=remote.name,
            backend=self.backend,
            uri=remote.uri,
            requires_credentials=False,
            fallback_uri=str(fallback_dir),
            setup_commands=[
                f"dvc remote add -d {remote.name} {remote.uri}",
                f"mkdir {fallback_dir.name}",
            ],
        )


class CloudAdapter:
    def __init__(self, backend: str) -> None:
        self.backend = backend

    def build_plan(self, remote: RemoteDefinition, base_dir: Path) -> RemotePlan:
        fallback_dir = base_dir / ".demo-remotes" / remote.name
        return RemotePlan(
            name=remote.name,
            backend=self.backend,
            uri=remote.uri,
            requires_credentials=True,
            fallback_uri=str(fallback_dir),
            setup_commands=[
                f"dvc remote add -d {remote.name} {remote.uri}",
                f"dvc remote modify {remote.name} credentialpath ./secrets/{remote.name}.json",
                f"dvc remote add {remote.name}-offline {fallback_dir}",
            ],
        )


def select_adapter(uri: str) -> RemoteAdapter:
    """Seleciona o adapter apropriado pelo prefixo do URI."""

    if uri.startswith("s3://"):
        return CloudAdapter("s3")
    if uri.startswith("gs://"):
        return CloudAdapter("gcs")
    return LocalAdapter()


def build_remote_plan(remote: RemoteDefinition, base_dir: Path | None = None) -> RemotePlan:
    """Facade simples para montar o plano final do remoto."""

    workspace = base_dir or Path(__file__).resolve().parent
    adapter = select_adapter(remote.uri)
    return adapter.build_plan(remote, workspace)


def build_demo_plans() -> list[RemotePlan]:
    """Constroi tres cenarios para a aula."""

    base_dir = Path(__file__).resolve().parent
    remotes = [
        RemoteDefinition(name="local-cache", uri="./artifacts/dvc-cache"),
        RemoteDefinition(name="team-s3", uri="s3://mlet-demo/dvc-cache"),
        RemoteDefinition(name="team-gcs", uri="gs://mlet-demo/dvc-cache"),
    ]
    return [build_remote_plan(remote, base_dir) for remote in remotes]


if __name__ == "__main__":
    print(json.dumps([asdict(item) for item in build_demo_plans()], indent=2, ensure_ascii=False))