"""Aula 05 - state pattern para registry local de modelos."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum


class StageName(StrEnum):
    """Estagios simplificados do registry."""

    NONE = "none"
    STAGING = "staging"
    PRODUCTION = "production"
    ARCHIVED = "archived"


@dataclass(frozen=True, slots=True)
class TransitionRecord:
    """Representa uma transicao realizada no registry."""

    from_stage: str
    to_stage: str
    reason: str


@dataclass(slots=True)
class ModelVersion:
    """Versao simplificada de um modelo registrado."""

    version: str
    validation_score: float
    stage: StageName = StageName.NONE
    history: list[TransitionRecord] = field(default_factory=list)


class RegistryState:
    """Estado base com regra de transicao."""

    stage = StageName.NONE

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        raise NotImplementedError


class DraftState(RegistryState):
    stage = StageName.NONE

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        if target is not StageName.STAGING:
            raise ValueError("Versoes novas so podem ir para staging primeiro")
        _transition(model, self.stage, target, reason)


class StagingState(RegistryState):
    stage = StageName.STAGING

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        if target not in {StageName.PRODUCTION, StageName.ARCHIVED}:
            raise ValueError("Staging so promove para production ou archived")
        _transition(model, self.stage, target, reason)


class ProductionState(RegistryState):
    stage = StageName.PRODUCTION

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        if target is not StageName.ARCHIVED:
            raise ValueError("Production so pode ser arquivado neste demonstrador")
        _transition(model, self.stage, target, reason)


class ArchivedState(RegistryState):
    stage = StageName.ARCHIVED

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        raise ValueError("Versao arquivada nao volta ao fluxo ativo neste demonstrador")


def _transition(model: ModelVersion, source: StageName, target: StageName, reason: str) -> None:
    model.stage = target
    model.history.append(
        TransitionRecord(from_stage=source.value, to_stage=target.value, reason=reason)
    )


def state_for(stage: StageName) -> RegistryState:
    """Resolve o estado atual para o objeto correspondente."""

    states = {
        StageName.NONE: DraftState(),
        StageName.STAGING: StagingState(),
        StageName.PRODUCTION: ProductionState(),
        StageName.ARCHIVED: ArchivedState(),
    }
    return states[stage]


class LocalModelRegistry:
    """Registry local para a aula, sem dependencia de servidor externo."""

    def __init__(self) -> None:
        self.versions: list[ModelVersion] = []

    def register(self, version: str, validation_score: float) -> ModelVersion:
        model = ModelVersion(version=version, validation_score=validation_score)
        self.versions.append(model)
        return model

    def promote(self, model: ModelVersion, target: StageName, reason: str) -> None:
        current_state = state_for(model.stage)
        current_state.promote(model, target, reason)

    def snapshot(self) -> dict[str, object]:
        production = [model.version for model in self.versions if model.stage is StageName.PRODUCTION]
        archived = [model.version for model in self.versions if model.stage is StageName.ARCHIVED]
        staging = [model.version for model in self.versions if model.stage is StageName.STAGING]
        return {
            "production": production,
            "staging": staging,
            "archived": archived,
            "versions": [asdict(version) for version in self.versions],
        }


def run_registry_demo() -> dict[str, object]:
    """Executa o fluxo completo de registro e promocao."""

    registry = LocalModelRegistry()
    champion = registry.register(version="model-v1", validation_score=0.83)
    candidate = registry.register(version="model-v2", validation_score=0.89)

    registry.promote(champion, StageName.STAGING, "baseline inicial")
    registry.promote(champion, StageName.PRODUCTION, "baseline aprovada")
    registry.promote(candidate, StageName.STAGING, "nova candidata com melhor score")
    registry.promote(champion, StageName.ARCHIVED, "substituida pela nova versao")
    registry.promote(candidate, StageName.PRODUCTION, "promocao apos validacao")
    return registry.snapshot()


if __name__ == "__main__":
    print(json.dumps(run_registry_demo(), indent=2, ensure_ascii=False))