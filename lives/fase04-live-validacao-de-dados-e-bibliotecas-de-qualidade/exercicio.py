"""Exercício prático — Validação de Dados e Bibliotecas de Qualidade

Fase 04 | Live de Hands-on
Disciplina: fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade

Conceitos-chave:
  - Great Expectations suites
  - Pandera schemas
  - Pydantic runtime
  - Quality gates
  - Pipeline e2e de validação

Exercícios propostos:
  1. Criar suite GE para dataset de churn
  2. Definir schema Pandera com checks customizados
  3. Implementar quality gate bloqueante em pipeline
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Validação de Dados e Bibliotecas de Qualidade ===")
    logger.info("Fase: 04")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar suite GE para dataset de churn")
    logger.info("  2. Definir schema Pandera com checks customizados")
    logger.info("  3. Implementar quality gate bloqueante em pipeline")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade")


if __name__ == "__main__":
    main()
