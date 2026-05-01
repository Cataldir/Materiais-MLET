"""Exercício prático — Deploy de Agentes com LLMs

Fase 05 | Live de Hands-on
Disciplina: fase-05-deploy-avancado-de-ia-generativa/02-deploy-agentes-llms

Conceitos-chave:
  - Agentes com tools
  - RAG pipeline
  - Tracing de agentes
  - Deploy de agente como API
  - Projeto completo

Exercícios propostos:
  1. Criar agente com tool de knowledge base
  2. Implementar RAG com retrieval + generation
  3. Deploy de agente como serviço REST
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Deploy de Agentes com LLMs ===")
    logger.info("Fase: 05")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar agente com tool de knowledge base")
    logger.info("  2. Implementar RAG com retrieval + generation")
    logger.info("  3. Deploy de agente como serviço REST")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-05-deploy-avancado-de-ia-generativa/02-deploy-agentes-llms")


if __name__ == "__main__":
    main()
