"""DAGs e SCMs com simulacao deterministica de intervencoes."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

import numpy as np

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 27


@dataclass(frozen=True, slots=True)
class CausalEdge:
    """Aresta direcionada de um DAG causal."""

    source: str
    target: str


@dataclass(frozen=True, slots=True)
class CausalGraph:
    """Representacao simples do grafo causal."""

    nodes: tuple[str, ...]
    edges: tuple[CausalEdge, ...]


@dataclass(frozen=True, slots=True)
class InterventionSummary:
    """Resumo do efeito de uma intervencao."""

    strategy: str
    treatment_value: float
    average_outcome: float


class InterventionStrategy(Protocol):
    """Contrato para estrategias de intervencao."""

    name: str

    def simulate(self, scm: StructuralCausalModel) -> InterventionSummary:
        """Executa a intervencao sobre o SCM."""


class CausalGraphBuilder:
    """Builder explicito para o grafo causal da aula."""

    def __init__(self) -> None:
        self._nodes: list[str] = []
        self._edges: list[CausalEdge] = []

    def add_node(self, node: str) -> CausalGraphBuilder:
        self._nodes.append(node)
        return self

    def add_edge(self, source: str, target: str) -> CausalGraphBuilder:
        self._edges.append(CausalEdge(source=source, target=target))
        return self

    def build(self) -> CausalGraph:
        return CausalGraph(nodes=tuple(self._nodes), edges=tuple(self._edges))


class StructuralCausalModel:
    """SCM sintetico para campanha e conversao."""

    def __init__(self, sample_size: int = 2000, seed: int = RANDOM_STATE) -> None:
        self.sample_size = sample_size
        self.seed = seed

    def sample(self, treatment_override: float | None = None) -> dict[str, np.ndarray]:
        rng = np.random.default_rng(self.seed)
        engagement = rng.normal(0.0, 1.0, size=self.sample_size)
        tenure = rng.integers(1, 49, size=self.sample_size)
        base_propensity = 1.0 / (1.0 + np.exp(-(0.8 * engagement + 0.03 * tenure - 0.4)))
        if treatment_override is None:
            treatment = rng.binomial(1, base_propensity)
        else:
            treatment = np.full(self.sample_size, fill_value=treatment_override)
        revenue = 120 + 25 * engagement + 1.6 * tenure + 42 * treatment + rng.normal(0, 8, size=self.sample_size)
        return {
            "engagement": engagement,
            "tenure": tenure.astype(float),
            "treatment": treatment.astype(float),
            "revenue": revenue,
        }


class TreatAllStrategy:
    """Intervencao do tipo tratar todos."""

    name = "treat_all"

    def simulate(self, scm: StructuralCausalModel) -> InterventionSummary:
        sample = scm.sample(treatment_override=1.0)
        return InterventionSummary(
            strategy=self.name,
            treatment_value=1.0,
            average_outcome=float(sample["revenue"].mean()),
        )


class TreatNoneStrategy:
    """Intervencao do tipo nao tratar ninguem."""

    name = "treat_none"

    def simulate(self, scm: StructuralCausalModel) -> InterventionSummary:
        sample = scm.sample(treatment_override=0.0)
        return InterventionSummary(
            strategy=self.name,
            treatment_value=0.0,
            average_outcome=float(sample["revenue"].mean()),
        )


def build_demo_graph() -> CausalGraph:
    """Constroi o grafo causal usado na aula."""

    return (
        CausalGraphBuilder()
        .add_node("engagement")
        .add_node("tenure")
        .add_node("treatment")
        .add_node("revenue")
        .add_edge("engagement", "treatment")
        .add_edge("tenure", "treatment")
        .add_edge("engagement", "revenue")
        .add_edge("tenure", "revenue")
        .add_edge("treatment", "revenue")
        .build()
    )


def run_dag_lesson() -> dict[str, object]:
    """Executa a simulacao principal da aula."""

    scm = StructuralCausalModel()
    strategies: tuple[InterventionStrategy, ...] = (TreatNoneStrategy(), TreatAllStrategy())
    interventions = tuple(strategy.simulate(scm) for strategy in strategies)
    estimated_effect = interventions[1].average_outcome - interventions[0].average_outcome
    return {
        "graph": build_demo_graph(),
        "interventions": interventions,
        "estimated_effect": estimated_effect,
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_dag_lesson()
    LOGGER.info("nodes=%s", summary["graph"].nodes)
    LOGGER.info("edges=%s", [(edge.source, edge.target) for edge in summary["graph"].edges])
    for intervention in summary["interventions"]:
        LOGGER.info(
            "%s | treatment=%.0f | average_outcome=%.2f",
            intervention.strategy,
            intervention.treatment_value,
            intervention.average_outcome,
        )
    LOGGER.info("estimated_effect=%.2f", summary["estimated_effect"])


if __name__ == "__main__":
    main()