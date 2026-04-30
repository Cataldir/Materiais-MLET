"""Exercício prático — Monitoração de Performance + Serviços de Monitoração

Fase 03 | Live de Hands-on
Disciplina: fase-03-deploy-e-servir-modelos/04-monitoracao-performance

Conceitos-chave:
  - Prometheus + Grafana
  - Métricas de latência e throughput
  - Alertas de degradação
  - SLIs/SLOs para ML
  - ELK stack

Exercícios propostos:
  1. Instrumentar API com métricas Prometheus
  2. Criar dashboard Grafana para modelo em produção
  3. Configurar alertas de degradação
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Monitoração de Performance + Serviços de Monitoração ===")
    logger.info("Fase: 03")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Instrumentar API com métricas Prometheus")
    logger.info("  2. Criar dashboard Grafana para modelo em produção")
    logger.info("  3. Configurar alertas de degradação")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-03-deploy-e-servir-modelos/04-monitoracao-performance")


if __name__ == "__main__":
    main()
