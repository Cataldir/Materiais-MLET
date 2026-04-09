"""
Detecção de Data Drift via Kolmogorov-Smirnov test.

Compara distribuição de features em produção contra dados de referência
(salvos durante o treino) e emite métricas Prometheus.
"""

import logging
from pathlib import Path

import numpy as np
from scipy import stats

from src.common.config import settings
from src.common.metrics import FEATURE_DRIFT_PVALUE, FEATURE_DRIFT_SCORE

logger = logging.getLogger(__name__)


class DriftDetector:
    """Detecta data drift comparando dados de produção vs. referência."""

    def __init__(self, reference_path: str | None = None, threshold: float | None = None):
        self.reference_path = Path(reference_path or settings.REFERENCE_DATA_PATH)
        self.threshold = threshold or settings.DRIFT_THRESHOLD
        self._reference_data: np.ndarray | None = None
        self._feature_names: list[str] = []

    def load_reference(self) -> bool:
        """Carrega dados de referência salvos durante o treino."""
        if not self.reference_path.exists():
            logger.warning("Arquivo de referência não encontrado: %s", self.reference_path)
            return False

        ref = np.load(self.reference_path, allow_pickle=True)
        self._reference_data = ref["data"]
        self._feature_names = list(ref["feature_names"])
        logger.info(
            "Referência carregada: %d amostras, %d features",
            len(self._reference_data),
            len(self._feature_names),
        )
        return True

    def check_drift(self, production_data: np.ndarray) -> dict[str, dict]:
        """
        Executa teste KS para cada feature e emite métricas Prometheus.

        Returns:
            Dicionário {feature_name: {ks_statistic, p_value, drift_detected}}
        """
        if self._reference_data is None:
            if not self.load_reference():
                return {}

        results = {}
        for i, name in enumerate(self._feature_names):
            if i >= production_data.shape[1]:
                break

            ref_col = self._reference_data[:, i]
            prod_col = production_data[:, i]

            statistic, p_value = stats.ks_2samp(ref_col, prod_col)
            drift_detected = statistic > self.threshold

            # Emit Prometheus metrics
            FEATURE_DRIFT_SCORE.labels(feature_name=name).set(statistic)
            FEATURE_DRIFT_PVALUE.labels(feature_name=name).set(p_value)

            results[name] = {
                "ks_statistic": float(statistic),
                "p_value": float(p_value),
                "drift_detected": drift_detected,
            }

            if drift_detected:
                logger.warning(
                    "DRIFT DETECTADO em '%s': KS=%.4f (threshold=%.4f), p=%.4f",
                    name,
                    statistic,
                    self.threshold,
                    p_value,
                )

        drifted = [n for n, r in results.items() if r["drift_detected"]]
        if drifted:
            logger.warning("Features com drift: %s", drifted)
        else:
            logger.info("Nenhum drift detectado em %d features", len(results))

        return results
