"""Exercício prático — Segurança, Guardrails e Conformidade para LLMs

Fase 05 | Live de Hands-on
Disciplina: fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade

Conceitos-chave:
  - Guardrails de input/output
  - OWASP Top 10 para LLMs
  - Red teaming
  - Content filtering
  - System cards

Exercícios propostos:
  1. Implementar guardrails de input e output
  2. Mapear 5 ameaças OWASP para aplicação RAG
  3. Executar 5 cenários de red teaming
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Segurança, Guardrails e Conformidade para LLMs ===")
    logger.info("Fase: 05")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Implementar guardrails de input e output")
    logger.info("  2. Mapear 5 ameaças OWASP para aplicação RAG")
    logger.info("  3. Executar 5 cenários de red teaming")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-05-llms-e-agentes/05-seguranca-guardrails-conformidade")


if __name__ == "__main__":
    main()
