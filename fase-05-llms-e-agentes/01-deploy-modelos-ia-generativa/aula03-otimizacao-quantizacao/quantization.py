from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Protocol


@dataclass(frozen=True)
class ModelProfile:
    """Perfil simplificado de um modelo generativo."""

    name: str
    parameters_billion: float
    context_window: int
    quality_sensitivity: str


@dataclass(frozen=True)
class HardwareProfile:
    """Recursos locais disponiveis para serving."""

    name: str
    memory_gb: int
    compute_tier: str
    latency_budget_ms: int


@dataclass(frozen=True)
class OptimizationPlan:
    """Plano final de otimizacao para um perfil de modelo."""

    model_name: str
    hardware_name: str
    strategy_name: str
    estimated_memory_gb: float
    estimated_latency_ms: float
    expected_quality_loss: float
    rationale: str


class QuantizationStrategy(Protocol):
    """PEP 544: contrato estrutural para estrategias de compressao."""

    name: str

    def plan(
        self,
        model: ModelProfile,
        hardware: HardwareProfile,
    ) -> OptimizationPlan:
        """Constroi um plano de otimizacao para o modelo."""


class GptqStrategy:
    """Strategy: maximiza compressao quando a memoria e restrita."""

    name = "gptq"

    def plan(self, model: ModelProfile, hardware: HardwareProfile) -> OptimizationPlan:
        memory = round(max(2.8, model.parameters_billion * 0.72), 1)
        latency = round(58 + model.parameters_billion * 6.5, 1)
        quality_loss = 0.12 if model.quality_sensitivity == "high" else 0.08
        return OptimizationPlan(
            model_name=model.name,
            hardware_name=hardware.name,
            strategy_name=self.name,
            estimated_memory_gb=memory,
            estimated_latency_ms=latency,
            expected_quality_loss=quality_loss,
            rationale="Prioriza footprint agressivo para caber em memoria local limitada.",
        )


class AwqStrategy:
    """Strategy: prefere equilibrio entre latencia e preservacao de qualidade."""

    name = "awq"

    def plan(self, model: ModelProfile, hardware: HardwareProfile) -> OptimizationPlan:
        memory = round(max(3.4, model.parameters_billion * 0.84), 1)
        latency = round(50 + model.parameters_billion * 5.2, 1)
        quality_loss = 0.07 if model.quality_sensitivity == "high" else 0.05
        return OptimizationPlan(
            model_name=model.name,
            hardware_name=hardware.name,
            strategy_name=self.name,
            estimated_memory_gb=memory,
            estimated_latency_ms=latency,
            expected_quality_loss=quality_loss,
            rationale="Mantem melhor estabilidade para modelos sensiveis a degradacao.",
        )


class BitsAndBytesStrategy:
    """Strategy: opcao conservadora para setups simples e CPU-first."""

    name = "bitsandbytes"

    def plan(self, model: ModelProfile, hardware: HardwareProfile) -> OptimizationPlan:
        memory = round(max(4.0, model.parameters_billion * 0.96), 1)
        latency = round(46 + model.parameters_billion * 5.8, 1)
        quality_loss = 0.04 if model.quality_sensitivity == "high" else 0.03
        return OptimizationPlan(
            model_name=model.name,
            hardware_name=hardware.name,
            strategy_name=self.name,
            estimated_memory_gb=memory,
            estimated_latency_ms=latency,
            expected_quality_loss=quality_loss,
            rationale="Entrega compressao moderada com menor risco operacional em ambiente local.",
        )


class OptimizationAdvisor:
    """Template Method: define o fluxo fixo de recomendacao."""

    def __init__(self, strategies: list[QuantizationStrategy]) -> None:
        self._strategies = {strategy.name: strategy for strategy in strategies}

    def build_plan(
        self,
        model: ModelProfile,
        hardware: HardwareProfile,
    ) -> OptimizationPlan:
        strategy = self.select_strategy(model, hardware)
        plan = strategy.plan(model, hardware)
        return self._adjust_for_constraints(plan, hardware)

    def select_strategy(
        self,
        model: ModelProfile,
        hardware: HardwareProfile,
    ) -> QuantizationStrategy:
        if hardware.memory_gb <= 12:
            return self._strategies["gptq"]
        if model.quality_sensitivity == "high" or hardware.latency_budget_ms <= 80:
            return self._strategies["awq"]
        return self._strategies["bitsandbytes"]

    def _adjust_for_constraints(
        self,
        plan: OptimizationPlan,
        hardware: HardwareProfile,
    ) -> OptimizationPlan:
        latency_penalty = 1.0
        if hardware.compute_tier == "cpu":
            latency_penalty = 1.25
        adjusted_latency = round(plan.estimated_latency_ms * latency_penalty, 1)
        rationale = plan.rationale
        if adjusted_latency > hardware.latency_budget_ms:
            rationale = rationale + " Ajuste: latencia excede o budget e exige batching ou cache local."
        return OptimizationPlan(
            model_name=plan.model_name,
            hardware_name=plan.hardware_name,
            strategy_name=plan.strategy_name,
            estimated_memory_gb=plan.estimated_memory_gb,
            estimated_latency_ms=adjusted_latency,
            expected_quality_loss=plan.expected_quality_loss,
            rationale=rationale,
        )


MODELS = [
    ModelProfile("support-3b", parameters_billion=3.0, context_window=4096, quality_sensitivity="medium"),
    ModelProfile("ops-7b", parameters_billion=7.0, context_window=8192, quality_sensitivity="high"),
    ModelProfile("analytics-13b", parameters_billion=13.0, context_window=8192, quality_sensitivity="medium"),
]

HARDWARE = {
    "edge_laptop": HardwareProfile("edge_laptop", memory_gb=12, compute_tier="cpu", latency_budget_ms=120),
    "studio_gpu": HardwareProfile("studio_gpu", memory_gb=24, compute_tier="gpu", latency_budget_ms=95),
}


def recommend_optimization_plans(hardware_name: str = "studio_gpu") -> list[OptimizationPlan]:
    """Gera recomendacoes deterministicas para os perfis da aula."""

    advisor = OptimizationAdvisor(
        [GptqStrategy(), AwqStrategy(), BitsAndBytesStrategy()]
    )
    hardware = HARDWARE[hardware_name]
    return [advisor.build_plan(model, hardware) for model in MODELS]


def main() -> None:
    plans = recommend_optimization_plans()
    for plan in plans:
        print(asdict(plan))


if __name__ == "__main__":
    main()