"""Exercício prático — Docker e Kubernetes

Fase 02 | Live de Hands-on
Disciplina: fase-02-containers-e-ambientes-reprodutiveis/03-docker-kubernetes

Conceitos-chave:
  - Dockerfile multi-stage
  - Docker Compose
  - K8s Deployment + Service
  - HPA
  - Helm charts

Exercícios propostos:
  1. Criar Dockerfile multi-stage para API de inferência
  2. Compor API + modelo + banco com Docker Compose
  3. Deploy em K8s com HPA
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Docker e Kubernetes ===")
    logger.info("Fase: 02")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Criar Dockerfile multi-stage para API de inferência")
    logger.info("  2. Compor API + modelo + banco com Docker Compose")
    logger.info("  3. Deploy em K8s com HPA")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-02-containers-e-ambientes-reprodutiveis/03-docker-kubernetes")


if __name__ == "__main__":
    main()
