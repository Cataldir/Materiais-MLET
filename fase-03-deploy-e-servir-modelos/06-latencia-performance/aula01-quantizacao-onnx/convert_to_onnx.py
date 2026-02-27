"""Conversão de modelos para ONNX — otimização de latência de inferência.

Demonstra como converter modelos sklearn e PyTorch para ONNX
para inferência otimizada em produção.

Requisitos:
    pip install onnx onnxruntime skl2onnx

Uso:
    python convert_to_onnx.py --model models/model.pkl --output models/model.onnx
"""

import logging
import time
from pathlib import Path

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

N_BENCHMARK_RUNS = 100


def convert_sklearn_to_onnx(model_path: Path, output_path: Path, n_features: int = 4) -> Path:
    """Converte modelo sklearn para ONNX.

    Args:
        model_path: Caminho para o modelo .pkl.
        output_path: Caminho de saída para o .onnx.
        n_features: Número de features de entrada.

    Returns:
        Caminho para o modelo ONNX criado.
    """
    try:
        import pickle
        from skl2onnx import convert_sklearn
        from skl2onnx.common.data_types import FloatTensorType

        with open(model_path, "rb") as f:
            model = pickle.load(f)  # noqa: S301

        initial_type = [("float_input", FloatTensorType([None, n_features]))]
        onnx_model = convert_sklearn(model, initial_types=initial_type)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "wb") as f:
            f.write(onnx_model.SerializeToString())

        logger.info("Modelo convertido para ONNX: %s", output_path)
        return output_path
    except ImportError as exc:
        logger.error("Dependência não instalada: %s", exc)
        raise


def benchmark_inference(
    sklearn_model: object,
    onnx_path: Path,
    X_test: np.ndarray,
    n_runs: int = N_BENCHMARK_RUNS,
) -> dict[str, float]:
    """Compara latência entre sklearn e ONNX.

    Args:
        sklearn_model: Modelo sklearn original.
        onnx_path: Caminho para o modelo ONNX.
        X_test: Dados de teste para benchmark.
        n_runs: Número de execuções para média.

    Returns:
        Dicionário com latências médias em ms.
    """
    sklearn_times = []
    for _ in range(n_runs):
        start = time.perf_counter()
        sklearn_model.predict(X_test[:1])
        sklearn_times.append((time.perf_counter() - start) * 1000)

    onnx_times = []
    try:
        import onnxruntime as ort
        session = ort.InferenceSession(str(onnx_path))
        input_name = session.get_inputs()[0].name
        X_float = X_test[:1].astype(np.float32)

        for _ in range(n_runs):
            start = time.perf_counter()
            session.run(None, {input_name: X_float})
            onnx_times.append((time.perf_counter() - start) * 1000)
    except ImportError:
        logger.warning("onnxruntime não disponível")
        onnx_times = [0.0]

    result = {
        "sklearn_mean_ms": float(np.mean(sklearn_times)),
        "sklearn_p99_ms": float(np.percentile(sklearn_times, 99)),
        "onnx_mean_ms": float(np.mean(onnx_times)),
        "onnx_p99_ms": float(np.percentile(onnx_times, 99)),
    }

    if onnx_times[0] > 0:
        result["speedup"] = result["sklearn_mean_ms"] / result["onnx_mean_ms"]
        logger.info(
            "sklearn: %.3fms | ONNX: %.3fms | Speedup: %.2fx",
            result["sklearn_mean_ms"], result["onnx_mean_ms"], result["speedup"]
        )
    return result


def main() -> None:
    """Executa conversão e benchmark de um modelo demo."""
    import argparse
    import pickle
    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier

    parser = argparse.ArgumentParser(description="Converter modelo para ONNX")
    parser.add_argument("--model", type=Path, default=Path("models/model.pkl"))
    parser.add_argument("--output", type=Path, default=Path("models/model.onnx"))
    args = parser.parse_args()

    if not args.model.exists():
        logger.info("Treinando modelo demo...")
        X, y = load_iris(return_X_y=True)
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)
        args.model.parent.mkdir(exist_ok=True)
        with open(args.model, "wb") as f:
            pickle.dump(model, f)

    try:
        onnx_path = convert_sklearn_to_onnx(args.model, args.output, n_features=4)
        with open(args.model, "rb") as f:
            sklearn_model = pickle.load(f)  # noqa: S301
        X_test, _ = load_iris(return_X_y=True)
        benchmark_inference(sklearn_model, onnx_path, X_test)
    except Exception as exc:
        logger.error("Falha na conversão: %s", exc)


if __name__ == "__main__":
    main()
