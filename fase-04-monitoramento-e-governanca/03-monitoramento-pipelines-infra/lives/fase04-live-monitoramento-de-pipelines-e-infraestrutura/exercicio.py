"""Exercício prático — Monitoramento de Pipelines e Infraestrutura

Fase 04 | Live de Hands-on
Disciplina: fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra

Conceitos-chave:
  - OpenTelemetry spans
  - Tracing distribuído
  - Prometheus para infra
  - MLflow + monitoramento
  - Alertas operacionais

Exercícios propostos:
  1. Instrumentar pipeline com spans OpenTelemetry
  2. Criar trace completo de treino → deploy
  3. Configurar alertas de uso de recursos
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Monitoramento de Pipelines e Infraestrutura ===")
    logger.info("Fase: 04")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Instrumentar pipeline com spans OpenTelemetry")
    logger.info("  2. Criar trace completo de treino → deploy")
    logger.info("  3. Configurar alertas de uso de recursos")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra")


if __name__ == "__main__":
    main()
