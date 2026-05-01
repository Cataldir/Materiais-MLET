"""Exercício prático — Engenharia de Software para Cientistas de Dados

Fase 01 | Live de Hands-on
Disciplina: fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados

Conceitos-chave:
  - SOLID aplicado a ML
  - pytest e pandera
  - ruff e pre-commit
  - pyproject.toml
  - CLI com Pydantic Settings

Exercícios propostos:
  1. Refatorar pipeline monolítico aplicando SRP
  2. Criar suíte de testes com pytest para pipeline de features
  3. Configurar pre-commit hooks com ruff
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Engenharia de Software para Cientistas de Dados ===")
    logger.info("Fase: 01")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Refatorar pipeline monolítico aplicando SRP")
    logger.info("  2. Criar suíte de testes com pytest para pipeline de features")
    logger.info("  3. Configurar pre-commit hooks com ruff")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados")


if __name__ == "__main__":
    main()
