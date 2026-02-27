"""Batch inference — inferência em lote para modelos de ML.

Demonstra como processar grandes volumes de dados de forma eficiente
usando chunks e salvando resultados em arquivos.

Uso:
    python batch_inference.py --input data/input.csv --output data/predictions.csv
"""

import argparse
import logging
import pickle
import time
from pathlib import Path

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

CHUNK_SIZE = 1000
MODEL_PATH = Path("models/model.pkl")


def load_model(model_path: Path) -> object:
    """Carrega modelo serializado do disco.

    Args:
        model_path: Caminho para o arquivo .pkl do modelo.

    Returns:
        Modelo sklearn carregado.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
    """
    if not model_path.exists():
        raise FileNotFoundError(f"Modelo não encontrado: {model_path}")
    with open(model_path, "rb") as f:
        model = pickle.load(f)  # noqa: S301
    logger.info("Modelo carregado de: %s", model_path)
    return model


def process_chunk(chunk: pd.DataFrame, model: object) -> pd.DataFrame:
    """Processa um chunk de dados e gera predições.

    Args:
        chunk: DataFrame com features de entrada.
        model: Modelo treinado com método predict.

    Returns:
        DataFrame com coluna de predições adicionada.
    """
    features = chunk.select_dtypes(include=[np.number])
    predictions = model.predict(features)
    chunk = chunk.copy()
    chunk["prediction"] = predictions
    if hasattr(model, "predict_proba"):
        probas = model.predict_proba(features)
        chunk["prediction_proba"] = probas.max(axis=1)
    return chunk


def run_batch_inference(
    input_path: Path,
    output_path: Path,
    model_path: Path = MODEL_PATH,
    chunk_size: int = CHUNK_SIZE,
) -> None:
    """Executa inferência em lote processando o arquivo em chunks.

    Args:
        input_path: Caminho para o CSV de entrada.
        output_path: Caminho para salvar predições.
        model_path: Caminho para o modelo serializado.
        chunk_size: Número de linhas por chunk.
    """
    model = load_model(model_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    total_rows = 0
    start_time = time.perf_counter()
    first_chunk = True

    for chunk in pd.read_csv(input_path, chunksize=chunk_size):
        processed = process_chunk(chunk, model)
        processed.to_csv(
            output_path,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False,
        )
        total_rows += len(chunk)
        first_chunk = False
        logger.info("Processadas %d linhas...", total_rows)

    elapsed = time.perf_counter() - start_time
    logger.info("Concluído: %d linhas em %.2fs (%.0f linhas/s)",
                total_rows, elapsed, total_rows / elapsed)
    logger.info("Predições salvas em: %s", output_path)


def main() -> None:
    """Entry point CLI para inferência em lote."""
    parser = argparse.ArgumentParser(description="Batch inference para modelos sklearn")
    parser.add_argument("--input", type=Path, required=True, help="CSV de entrada")
    parser.add_argument("--output", type=Path, default=Path("data/predictions.csv"))
    parser.add_argument("--model", type=Path, default=MODEL_PATH)
    parser.add_argument("--chunk-size", type=int, default=CHUNK_SIZE)
    args = parser.parse_args()

    run_batch_inference(args.input, args.output, args.model, args.chunk_size)


if __name__ == "__main__":
    main()
