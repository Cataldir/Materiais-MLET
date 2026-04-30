"""Exercício prático — Aplicações Avançadas, Escalabilidade e LLMOps

Fase 05 | Live de Hands-on
Disciplina: fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade

Conceitos-chave:
  - Multi-agent orchestration
  - Stateful workflows
  - LLMOps
  - Escalabilidade horizontal
  - Projeto avançado

Exercícios propostos:
  1. Orquestrar 3 agentes com papéis distintos
  2. Implementar workflow stateful com checkpoints
  3. Benchmark de custo e latência
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Aplicações Avançadas, Escalabilidade e LLMOps ===")
    logger.info("Fase: 05")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Orquestrar 3 agentes com papéis distintos")
    logger.info("  2. Implementar workflow stateful com checkpoints")
    logger.info("  3. Benchmark de custo e latência")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade")


if __name__ == "__main__":
    main()
