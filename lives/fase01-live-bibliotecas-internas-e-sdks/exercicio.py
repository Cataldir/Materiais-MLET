"""Exercício prático — Bibliotecas Internas e SDKs

Fase 01 | Live de Hands-on
Disciplina: fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks

Conceitos-chave:
  - Layout src/
  - pyproject.toml
  - Semver
  - MkDocs
  - Formatação como contrato

Exercícios propostos:
  1. Criar pacote Python com layout src/
  2. Gerar documentação com MkDocs
  3. Configurar versionamento semântico
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Bibliotecas Internas e SDKs ===")
    logger.info("Fase: 01")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar pacote Python com layout src/")
    logger.info("  2. Gerar documentação com MkDocs")
    logger.info("  3. Configurar versionamento semântico")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks")


if __name__ == "__main__":
    main()
