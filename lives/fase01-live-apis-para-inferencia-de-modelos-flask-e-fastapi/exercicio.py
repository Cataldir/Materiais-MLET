"""Exercício prático — APIs para Inferência de Modelos (Flask e FastAPI)

Fase 01 | Live de Hands-on
Disciplina: fase-01-fundamentos-de-ml/04-apis-inferencia-modelos

Conceitos-chave:
  - Flask vs FastAPI
  - Pydantic para validação
  - Endpoint /predict
  - Middleware de logging
  - Testes de integração

Exercícios propostos:
  1. Criar API FastAPI com endpoint /predict
  2. Adicionar validação Pydantic para input/output
  3. Implementar health check e middleware de latência
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: APIs para Inferência de Modelos (Flask e FastAPI) ===")
    logger.info("Fase: 01")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar API FastAPI com endpoint /predict")
    logger.info("  2. Adicionar validação Pydantic para input/output")
    logger.info("  3. Implementar health check e middleware de latência")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-01-fundamentos-de-ml/04-apis-inferencia-modelos")


if __name__ == "__main__":
    main()
