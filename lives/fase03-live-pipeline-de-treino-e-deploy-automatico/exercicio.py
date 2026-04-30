"""Exercício prático — Pipeline de Treino e Deploy Automático

Fase 03 | Live de Hands-on
Disciplina: fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico

Conceitos-chave:
  - Pipeline end-to-end
  - Feature store
  - Airflow/Prefect
  - Automação de retreino
  - Canary deploy

Exercícios propostos:
  1. Construir pipeline e2e: ingest → features → train → deploy
  2. Simular feature store com point-in-time joins
  3. Implementar canary com rollback automático
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Pipeline de Treino e Deploy Automático ===")
    logger.info("Fase: 03")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Construir pipeline e2e: ingest → features → train → deploy")
    logger.info("  2. Simular feature store com point-in-time joins")
    logger.info("  3. Implementar canary com rollback automático")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico")


if __name__ == "__main__":
    main()
