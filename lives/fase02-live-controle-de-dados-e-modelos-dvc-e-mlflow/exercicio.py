"""Exercício prático — Controle de Dados e Modelos — DVC e MLflow

Fase 02 | Live de Hands-on
Disciplina: fase-02-containers-e-ambientes-reprodutiveis/04-dvc-mlflow

Conceitos-chave:
  - DVC pipelines
  - MLflow tracking
  - Model registry
  - Reprodutibilidade
  - CI/CD com DVC

Exercícios propostos:
  1. Configurar pipeline DVC para dataset + treino
  2. Registrar experimentos no MLflow
  3. Promover modelo no registry
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Controle de Dados e Modelos — DVC e MLflow ===")
    logger.info("Fase: 02")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Configurar pipeline DVC para dataset + treino")
    logger.info("  2. Registrar experimentos no MLflow")
    logger.info("  3. Promover modelo no registry")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-02-containers-e-ambientes-reprodutiveis/04-dvc-mlflow")


if __name__ == "__main__":
    main()
