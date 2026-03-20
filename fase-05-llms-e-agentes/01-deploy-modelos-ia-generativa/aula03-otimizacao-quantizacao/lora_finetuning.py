from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class LoRAConfig:
    """Configuracao local e simplificada para adaptacao LoRA."""

    name: str
    rank: int
    alpha: int
    target_modules: tuple[str, ...]
    estimated_trainable_millions: float
    adaptation_focus: str


@dataclass(frozen=True)
class LoRAOutcome:
    """Resultado heuristico de uma configuracao LoRA."""

    config_name: str
    expected_memory_delta_gb: float
    expected_latency_delta_ms: float
    expected_quality_gain: float


CONFIGS = [
    LoRAConfig(
        name="support_rank8",
        rank=8,
        alpha=16,
        target_modules=("q_proj", "v_proj"),
        estimated_trainable_millions=11.2,
        adaptation_focus="instruction_following",
    ),
    LoRAConfig(
        name="ops_rank16",
        rank=16,
        alpha=32,
        target_modules=("q_proj", "k_proj", "v_proj", "o_proj"),
        estimated_trainable_millions=22.4,
        adaptation_focus="domain_facts",
    ),
]


def compare_lora_configs() -> list[LoRAOutcome]:
    """Compara configuracoes LoRA usando heuristicas locais."""

    outcomes: list[LoRAOutcome] = []
    for config in CONFIGS:
        quality_gain = round(0.04 + config.rank / 400, 3)
        outcomes.append(
            LoRAOutcome(
                config_name=config.name,
                expected_memory_delta_gb=round(config.estimated_trainable_millions / 120, 3),
                expected_latency_delta_ms=round(3 + config.rank * 0.45, 1),
                expected_quality_gain=quality_gain,
            )
        )
    return outcomes


def main() -> None:
    for outcome in compare_lora_configs():
        print(asdict(outcome))


if __name__ == "__main__":
    main()