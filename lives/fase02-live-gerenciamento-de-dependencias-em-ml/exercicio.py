"""Exercício prático — Gerenciamento de Dependências em ML

Fase 02 | Live de Hands-on
Disciplina: fase-02-containers-e-ambientes-reprodutiveis/02-gerenciamento-dependencias

Conceitos-chave:
  - venv vs Poetry vs uv
  - Lock files
  - pyproject.toml
  - Constraints
  - Ambientes reproduzíveis

Exercícios propostos:
  1. Criar ambiente isolado com uv
  2. Gerar lock file e constraints
  3. Migrar requirements.txt para pyproject.toml
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Gerenciamento de Dependências em ML ===")
    logger.info("Fase: 02")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar ambiente isolado com uv")
    logger.info("  2. Gerar lock file e constraints")
    logger.info("  3. Migrar requirements.txt para pyproject.toml")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-02-containers-e-ambientes-reprodutiveis/02-gerenciamento-dependencias")


if __name__ == "__main__":
    main()
