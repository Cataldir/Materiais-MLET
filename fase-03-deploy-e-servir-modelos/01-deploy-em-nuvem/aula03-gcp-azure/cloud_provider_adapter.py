"""Comparativo local entre GCP e Azure com contrato de deploy compartilhado."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class DeploymentRequest:
    """Define o contrato minimo de um deploy comparavel entre provedores."""

    system_name: str
    region: str
    min_replicas: int
    max_replicas: int
    monthly_requests_millions: float


@dataclass(frozen=True, slots=True)
class ProviderPlan:
    """Resume como um provedor atende o mesmo contrato de deploy."""

    provider: str
    serving_service: str
    artifact_store: str
    observability_service: str
    autoscaling_policy: str
    deployment_command: str
    estimated_monthly_cost_usd: int


class CloudProviderAdapter(Protocol):
    """Adapter para traduzir o mesmo contrato para cada provedor."""

    provider_name: str

    def build_plan(self, request: DeploymentRequest) -> ProviderPlan:
        """Retorna o plano deterministico do provedor para o workload."""


class AzureProviderAdapter:
    """Mapeia o contrato para servicos equivalentes da Azure."""

    provider_name = "azure"

    def build_plan(self, request: DeploymentRequest) -> ProviderPlan:
        return ProviderPlan(
            provider=self.provider_name,
            serving_service="Azure Container Apps",
            artifact_store="Azure Blob Storage",
            observability_service="Azure Monitor",
            autoscaling_policy=(
                f"KEDA between {request.min_replicas} and {request.max_replicas} replicas"
            ),
            deployment_command="az containerapp up --source .",
            estimated_monthly_cost_usd=142,
        )


class GCPProviderAdapter:
    """Mapeia o contrato para servicos equivalentes da GCP."""

    provider_name = "gcp"

    def build_plan(self, request: DeploymentRequest) -> ProviderPlan:
        return ProviderPlan(
            provider=self.provider_name,
            serving_service="Cloud Run",
            artifact_store="Cloud Storage",
            observability_service="Cloud Monitoring",
            autoscaling_policy=(
                f"Autoscaling between {request.min_replicas} and {request.max_replicas} instances"
            ),
            deployment_command="gcloud run deploy local-model-api --source .",
            estimated_monthly_cost_usd=135,
        )


def compare_provider_plans() -> tuple[ProviderPlan, ...]:
    """Executa o comparativo local entre os adaptadores de provider."""

    request = DeploymentRequest(
        system_name="fraud-scoring-api",
        region="southamerica-east1",
        min_replicas=1,
        max_replicas=6,
        monthly_requests_millions=2.5,
    )
    adapters: tuple[CloudProviderAdapter, ...] = (
        AzureProviderAdapter(),
        GCPProviderAdapter(),
    )
    plans = tuple(adapter.build_plan(request) for adapter in adapters)
    return tuple(sorted(plans, key=lambda plan: plan.provider))


def main() -> None:
    """Imprime o comparativo de planos no terminal."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for plan in compare_provider_plans():
        LOGGER.info(
            "%s -> service=%s observability=%s cost=%susd",
            plan.provider,
            plan.serving_service,
            plan.observability_service,
            plan.estimated_monthly_cost_usd,
        )


if __name__ == "__main__":
    main()