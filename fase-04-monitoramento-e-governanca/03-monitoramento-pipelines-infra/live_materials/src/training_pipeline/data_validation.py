"""
Validação de dados com métricas Prometheus.

Verifica qualidade dos dados antes do treino,
emitindo métricas de nulos, outliers e schema.
"""

import logging

import numpy as np
from prometheus_client import Gauge

from src.common.metrics import DATA_MISSING_RATIO, DATA_OUTLIER_COUNT

logger = logging.getLogger(__name__)

SCHEMA_VALID = Gauge(
    "data_schema_valid",
    "1 se schema válido, 0 caso contrário",
    ["dataset_name"],
)

DATA_ROW_COUNT = Gauge(
    "data_row_count",
    "Número de linhas no dataset",
    ["dataset_name", "split"],
)


def validate_schema(
    X: np.ndarray,
    expected_features: int,
    dataset_name: str = "iris",
) -> bool:
    """Valida que o schema do dataset é o esperado."""
    valid = X.shape[1] == expected_features
    SCHEMA_VALID.labels(dataset_name=dataset_name).set(1 if valid else 0)
    if not valid:
        logger.error(
            "Schema inválido: esperado %d features, encontrado %d",
            expected_features,
            X.shape[1],
        )
    return valid


def check_missing_values(
    X: np.ndarray,
    feature_names: list[str],
    threshold: float = 0.05,
) -> dict[str, float]:
    """Verifica proporção de valores ausentes por feature."""
    results = {}
    for i, name in enumerate(feature_names):
        missing_ratio = np.isnan(X[:, i]).sum() / len(X)
        DATA_MISSING_RATIO.labels(feature_name=name).set(missing_ratio)
        results[name] = missing_ratio
        if missing_ratio > threshold:
            logger.warning(
                "Feature '%s' tem %.1f%% de valores ausentes (threshold: %.1f%%)",
                name,
                missing_ratio * 100,
                threshold * 100,
            )
    return results


def detect_outliers(
    X: np.ndarray,
    feature_names: list[str],
    z_threshold: float = 3.0,
) -> dict[str, int]:
    """Detecta outliers usando z-score por feature."""
    results = {}
    for i, name in enumerate(feature_names):
        col = X[:, i]
        mean, std = np.nanmean(col), np.nanstd(col)
        if std == 0:
            results[name] = 0
            continue
        z_scores = np.abs((col - mean) / std)
        outlier_count = int((z_scores > z_threshold).sum())
        DATA_OUTLIER_COUNT.labels(feature_name=name).inc(outlier_count)
        results[name] = outlier_count
        if outlier_count > 0:
            logger.info("Feature '%s': %d outliers detectados (z > %.1f)", name, outlier_count, z_threshold)
    return results


def run_validation(
    X: np.ndarray,
    feature_names: list[str],
    dataset_name: str = "iris",
    split: str = "train",
) -> bool:
    """Executa todas as validações e retorna True se dados são utilizáveis."""
    DATA_ROW_COUNT.labels(dataset_name=dataset_name, split=split).set(len(X))

    schema_ok = validate_schema(X, expected_features=len(feature_names), dataset_name=dataset_name)
    missing = check_missing_values(X, feature_names)
    outliers = detect_outliers(X, feature_names)

    high_missing = any(v > 0.05 for v in missing.values())
    many_outliers = any(v > len(X) * 0.05 for v in outliers.values())

    is_valid = schema_ok and not high_missing and not many_outliers
    logger.info(
        "Validação %s: schema=%s, missing_ok=%s, outliers_ok=%s",
        "PASSED" if is_valid else "FAILED",
        schema_ok,
        not high_missing,
        not many_outliers,
    )
    return is_valid
