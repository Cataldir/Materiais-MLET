"""Maquina de estados local para blue-green e canary deploy."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import StrEnum

LOGGER = logging.getLogger(__name__)
QUALITY_THRESHOLD = 0.88
ERROR_RATE_THRESHOLD = 0.03


class ReleaseMode(StrEnum):
    """Modos suportados pela simulacao local."""

    BLUE_GREEN = "blue_green"
    CANARY = "canary"


class ReleaseState(StrEnum):
    """Estados possiveis do ciclo de release."""

    CREATED = "created"
    VALIDATED = "validated"
    STAGED = "staged"
    CANARY = "canary"
    PROMOTED = "promoted"
    ROLLED_BACK = "rolled_back"


@dataclass(frozen=True, slots=True)
class ReleaseTransition:
    """Representa uma mudanca de estado da release."""

    state: ReleaseState
    message: str


@dataclass(frozen=True, slots=True)
class ReleaseSignal:
    """Metricas locais usadas para decidir promocao ou rollback."""

    quality_score: float
    canary_error_rate: float


class ReleaseStateMachine:
    """Controla a promocao do release de forma deterministica."""

    def __init__(self, mode: ReleaseMode, signal: ReleaseSignal) -> None:
        self.mode = mode
        self.signal = signal

    def run(self) -> tuple[ReleaseTransition, ...]:
        """Executa o fluxo de transicoes para o modo escolhido."""

        transitions = [
            ReleaseTransition(ReleaseState.CREATED, "release criada"),
        ]
        if self.signal.quality_score < QUALITY_THRESHOLD:
            transitions.append(
                ReleaseTransition(
                    ReleaseState.ROLLED_BACK,
                    "qualidade abaixo do minimo para prosseguir",
                )
            )
            return tuple(transitions)

        transitions.append(
            ReleaseTransition(ReleaseState.VALIDATED, "gates de qualidade aprovados")
        )
        transitions.append(
            ReleaseTransition(ReleaseState.STAGED, "release preparada no ambiente alvo")
        )
        if self.mode is ReleaseMode.CANARY:
            transitions.append(
                ReleaseTransition(ReleaseState.CANARY, "canary liberado para 10% do trafego")
            )
            if self.signal.canary_error_rate > ERROR_RATE_THRESHOLD:
                transitions.append(
                    ReleaseTransition(
                        ReleaseState.ROLLED_BACK,
                        "erro do canary acima do limite; rollback acionado",
                    )
                )
                return tuple(transitions)

        transitions.append(
            ReleaseTransition(ReleaseState.PROMOTED, "release promovida para 100%")
        )
        return tuple(transitions)


def simulate_release(
    mode: ReleaseMode,
    quality_score: float,
    canary_error_rate: float,
) -> tuple[ReleaseTransition, ...]:
    """Executa uma simulacao local de release."""

    machine = ReleaseStateMachine(
        mode=mode,
        signal=ReleaseSignal(
            quality_score=quality_score,
            canary_error_rate=canary_error_rate,
        ),
    )
    return machine.run()


def main() -> None:
    """Exibe um exemplo rapido de deploy continuo."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    transitions = simulate_release(ReleaseMode.CANARY, 0.92, 0.01)
    for transition in transitions:
        LOGGER.info("%s -> %s", transition.state, transition.message)


if __name__ == "__main__":
    main()