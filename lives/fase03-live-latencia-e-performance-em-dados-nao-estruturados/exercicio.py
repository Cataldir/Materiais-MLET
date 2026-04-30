"""Exercício prático — Latência e Performance em Dados Não Estruturados

Fase 03 | Live de Hands-on
Disciplina: fase-03-cloud-e-mlops/06-latencia-performance

Conceitos-chave:
  - Quantização INT8
  - ONNX Runtime
  - Triton/TorchServe
  - Pré-processamento otimizado
  - Benchmark e2e

Exercícios propostos:
  1. Converter modelo PyTorch para ONNX
  2. Benchmark: tempo de inferência original vs quantizado
  3. Pipeline de pré-processamento otimizado
"""

import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Ponto de entrada do exercício."""
    logger.info("=== Live: Latência e Performance em Dados Não Estruturados ===")
    logger.info("Fase: 03")
    logger.info("")
    logger.info("Exercícios:")
    logger.info("  1. Converter modelo PyTorch para ONNX")
    logger.info("  2. Benchmark: tempo de inferência original vs quantizado")
    logger.info("  3. Pipeline de pré-processamento otimizado")
    logger.info("")
    logger.info("Consulte o README para instruções detalhadas.")
    logger.info("Material de referência: fase-03-cloud-e-mlops/06-latencia-performance")


if __name__ == "__main__":
    main()
