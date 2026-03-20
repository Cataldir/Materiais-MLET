"""Comparacao local de servicos gerenciados de cloud monitoring."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ProviderSummary:
    """Resumo comparavel de um provedor de monitoring."""

    provider: str
    services: tuple[str, ...]
    local_command: str
    best_for: str


class MonitoringStrategy(Protocol):
    """Contrato comum para estrategias de comparacao por provedor."""

    provider_name: str

    def summarize(self) -> ProviderSummary:
        """Resume a stack gerenciada do provedor."""


class AWSMonitoringStrategy:
    """Estrategia para o ecossistema AWS."""

    provider_name = "aws"

    def summarize(self) -> ProviderSummary:
        return ProviderSummary(
            provider=self.provider_name,
            services=("CloudWatch", "CloudWatch Logs", "X-Ray"),
            local_command="aws cloudwatch describe-alarms",
            best_for="times pequenos que querem servico unificado na AWS",
        )


class GCPMonitoringStrategy:
    """Estrategia para o ecossistema GCP."""

    provider_name = "gcp"

    def summarize(self) -> ProviderSummary:
        return ProviderSummary(
            provider=self.provider_name,
            services=("Cloud Monitoring", "Cloud Logging", "Cloud Trace"),
            local_command="gcloud monitoring dashboards list",
            best_for="workloads serverless e times ja padronizados em GCP",
        )


class AzureMonitoringStrategy:
    """Estrategia para o ecossistema Azure."""

    provider_name = "azure"

    def summarize(self) -> ProviderSummary:
        return ProviderSummary(
            provider=self.provider_name,
            services=("Azure Monitor", "Log Analytics", "Application Insights"),
            local_command="az monitor metrics list-definitions --resource <id>",
            best_for="times que querem integracao forte com apps e recursos Azure",
        )


def compare_cloud_monitoring() -> tuple[ProviderSummary, ...]:
    """Executa o comparativo local entre provedores."""

    strategies: tuple[MonitoringStrategy, ...] = (
        AWSMonitoringStrategy(),
        GCPMonitoringStrategy(),
        AzureMonitoringStrategy(),
    )
    summaries = tuple(strategy.summarize() for strategy in strategies)
    return tuple(sorted(summaries, key=lambda summary: summary.provider))


def main() -> None:
    """Imprime o comparativo resumido de providers."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for summary in compare_cloud_monitoring():
        LOGGER.info("%s -> %s", summary.provider, summary.services[0])


if __name__ == "__main__":
    main()