"""Exercício prático — Governança, Compliance (LGPD/GDPR) e Inferência Causal

Fase 04 | Live de Hands-on
Disciplina: fase-04-monitoramento-e-governanca/05-governanca-compliance

Conceitos-chave:
  - Model cards
  - LGPD/GDPR para ML
  - Fairness e explicabilidade
  - DAGs causais
  - Inferência causal

Exercícios propostos:
  1. Gerar model card completo para modelo de crédito
  2. Mapear requisitos LGPD para pipeline de dados
  3. Construir DAG causal e estimar efeito de intervenção
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Governança, Compliance (LGPD/GDPR) e Inferência Causal ===")
    logger.info("Fase: 04")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Gerar model card completo para modelo de crédito")
    logger.info("  2. Mapear requisitos LGPD para pipeline de dados")
    logger.info("  3. Construir DAG causal e estimar efeito de intervenção")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-04-monitoramento-e-governanca/05-governanca-compliance")


if __name__ == "__main__":
    main()
