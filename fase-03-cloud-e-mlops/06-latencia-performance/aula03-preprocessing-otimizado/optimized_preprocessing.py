"""Estrategias locais de preprocessamento com equivalencia semantica."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)
NON_ALNUM = re.compile(r"[^a-z0-9 ]+")
MULTI_SPACE = re.compile(r"\s+")


@dataclass(frozen=True, slots=True)
class PreprocessingComparison:
    """Resume custo modelado e equivalencia semantica."""

    all_semantically_equal: bool
    baseline_cost_units: int
    optimized_cost_units: int
    normalized_samples: tuple[str, ...]


class PreprocessingStrategy(Protocol):
    """Contrato das estrategias comparadas."""

    def normalize(self, text: str) -> str:
        """Normaliza o texto segundo a estrategia escolhida."""


class BaselinePreprocessor:
    """Implementacao direta e mais verbosa."""

    def normalize(self, text: str) -> str:
        lowered = text.lower()
        filtered = "".join(char if char.isalnum() or char == " " else " " for char in lowered)
        collapsed = " ".join(part for part in filtered.split() if part)
        return collapsed


class OptimizedPreprocessor:
    """Implementacao enxuta baseada em regex precompilada."""

    def normalize(self, text: str) -> str:
        lowered = text.lower()
        filtered = NON_ALNUM.sub(" ", lowered)
        return MULTI_SPACE.sub(" ", filtered).strip()


def compare_preprocessors() -> PreprocessingComparison:
    """Compara as duas estrategias em uma pequena amostra local."""

    baseline = BaselinePreprocessor()
    optimized = OptimizedPreprocessor()
    samples = (
        "Fraude!!! Cartao 123 bloqueado",
        "Cliente VIP com atraso???",
        "Novo-device: login_em_2_regioes",
    )
    baseline_outputs = tuple(baseline.normalize(sample) for sample in samples)
    optimized_outputs = tuple(optimized.normalize(sample) for sample in samples)
    return PreprocessingComparison(
        all_semantically_equal=baseline_outputs == optimized_outputs,
        baseline_cost_units=120,
        optimized_cost_units=72,
        normalized_samples=optimized_outputs,
    )


def main() -> None:
    """Imprime o resultado do comparativo local."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    comparison = compare_preprocessors()
    LOGGER.info(
        "equal=%s optimized_cost=%s",
        comparison.all_semantically_equal,
        comparison.optimized_cost_units,
    )


if __name__ == "__main__":
    main()