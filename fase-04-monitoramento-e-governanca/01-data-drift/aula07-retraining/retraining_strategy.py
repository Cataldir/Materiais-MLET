"""Retraining Strategy — estratégias de retreinamento de modelos.

Implementa retreinamento periódico e baseado em trigger (quando drift
é detectado), com versionamento e validação antes de substituição.

Uso:
    python retraining_strategy.py
"""

import logging
from abc import ABC, abstractmethod
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
MIN_PERFORMANCE_THRESHOLD = 0.80
DRIFT_THRESHOLD = 0.1
MODELS_DIR = Path("models/versions")


class RetrainingStrategy(ABC):
    """Interface base para estratégias de retreinamento.

    Define o contrato para estratégias periódicas e baseadas em trigger.
    """

    @abstractmethod
    def should_retrain(self, **kwargs: Any) -> bool:
        """Determina se o modelo deve ser retreinado.

        Args:
            **kwargs: Argumentos específicos de cada estratégia.

        Returns:
            True se retreinamento é necessário.
        """

    @abstractmethod
    def get_strategy_name(self) -> str:
        """Retorna o nome da estratégia.

        Returns:
            Nome descritivo da estratégia.
        """


class PeriodicRetrainingStrategy(RetrainingStrategy):
    """Estratégia de retreinamento periódico por tempo ou volume de dados.

    Attributes:
        days_interval: Intervalo em dias entre retreinamentos.
        last_training_date: Data do último treino.
    """

    def __init__(self, days_interval: int = 7) -> None:
        """Inicializa estratégia periódica.

        Args:
            days_interval: Intervalo em dias entre retreinamentos.
        """
        self.days_interval = days_interval
        self.last_training_date: datetime = datetime.min

    def should_retrain(
        self, current_date: datetime | None = None, **kwargs: Any
    ) -> bool:
        """Verifica se o intervalo de tempo foi atingido.

        Args:
            current_date: Data atual (default: now).
            **kwargs: Argumentos adicionais ignorados.

        Returns:
            True se dias desde último treino >= intervalo.
        """
        now = current_date or datetime.now()
        days_elapsed = (now - self.last_training_date).days
        should = days_elapsed >= self.days_interval
        logger.info(
            "Periódico: %d dias desde último treino (intervalo: %d) → %s",
            days_elapsed,
            self.days_interval,
            "RETREINAR" if should else "aguardar",
        )
        return should

    def get_strategy_name(self) -> str:
        """Retorna nome da estratégia."""
        return f"Periódico ({self.days_interval} dias)"


class DriftTriggeredRetrainingStrategy(RetrainingStrategy):
    """Estratégia de retreinamento baseada em detecção de drift.

    Attributes:
        drift_threshold: Limiar PSI para trigger de retreinamento.
    """

    def __init__(self, drift_threshold: float = DRIFT_THRESHOLD) -> None:
        """Inicializa estratégia baseada em drift.

        Args:
            drift_threshold: PSI acima do qual o retreinamento é acionado.
        """
        self.drift_threshold = drift_threshold

    def should_retrain(self, psi_score: float = 0.0, **kwargs: Any) -> bool:
        """Verifica se o drift detectado excede o threshold.

        Args:
            psi_score: PSI calculado para os dados de produção.
            **kwargs: Argumentos adicionais ignorados.

        Returns:
            True se PSI >= threshold.
        """
        should = psi_score >= self.drift_threshold
        logger.info(
            "Drift trigger: PSI=%.4f (threshold=%.2f) → %s",
            psi_score,
            self.drift_threshold,
            "RETREINAR" if should else "OK",
        )
        return should

    def get_strategy_name(self) -> str:
        """Retorna nome da estratégia."""
        return f"Drift-triggered (PSI >= {self.drift_threshold})"


class PerformanceBasedRetrainingStrategy(RetrainingStrategy):
    """Estratégia baseada em queda de performance do modelo.

    Attributes:
        performance_threshold: AUC-ROC mínimo aceitável.
    """

    def __init__(
        self, performance_threshold: float = MIN_PERFORMANCE_THRESHOLD
    ) -> None:
        """Inicializa estratégia baseada em performance.

        Args:
            performance_threshold: AUC-ROC mínimo.
        """
        self.performance_threshold = performance_threshold

    def should_retrain(self, current_auc: float = 1.0, **kwargs: Any) -> bool:
        """Verifica se a performance caiu abaixo do threshold.

        Args:
            current_auc: AUC-ROC atual do modelo em produção.
            **kwargs: Argumentos adicionais ignorados.

        Returns:
            True se AUC < threshold.
        """
        should = current_auc < self.performance_threshold
        logger.info(
            "Performance: AUC=%.4f (threshold=%.2f) → %s",
            current_auc,
            self.performance_threshold,
            "RETREINAR" if should else "OK",
        )
        return should

    def get_strategy_name(self) -> str:
        """Retorna nome da estratégia."""
        return f"Performance-based (AUC < {self.performance_threshold})"


def retrain_model(
    X_new: np.ndarray,
    y_new: np.ndarray,
    version: str | None = None,
) -> tuple[RandomForestClassifier, dict[str, float]]:
    """Retreina e valida o modelo com novos dados.

    Args:
        X_new: Features para retreinamento.
        y_new: Labels para retreinamento.
        version: String de versão (default: timestamp).

    Returns:
        Tupla (modelo retreinado, métricas de validação).
    """
    version = version or datetime.now().strftime("%Y%m%d_%H%M%S")
    X_train, X_val, y_train, y_val = train_test_split(
        X_new, y_new, test_size=0.2, random_state=RANDOM_STATE, stratify=y_new
    )
    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)

    y_proba = model.predict_proba(X_val)[:, 1]
    auc = float(roc_auc_score(y_val, y_proba))
    metrics = {"auc_roc": auc, "version": version}

    if auc >= MIN_PERFORMANCE_THRESHOLD:
        MODELS_DIR.mkdir(parents=True, exist_ok=True)
        import pickle

        with open(MODELS_DIR / f"model_v{version}.pkl", "wb") as f:
            pickle.dump(model, f)
        logger.info("Modelo v%s salvo. AUC=%.4f ✓", version, auc)
    else:
        logger.warning(
            "Modelo v%s rejeitado. AUC=%.4f < %.2f",
            version,
            auc,
            MIN_PERFORMANCE_THRESHOLD,
        )

    return model, metrics


def demo_retraining_strategies() -> None:
    """Demonstra as três estratégias de retreinamento."""
    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target

    strategies: list[RetrainingStrategy] = [
        PeriodicRetrainingStrategy(days_interval=7),
        DriftTriggeredRetrainingStrategy(drift_threshold=0.1),
        PerformanceBasedRetrainingStrategy(performance_threshold=0.85),
    ]

    logger.info("=== Demonstração de Estratégias de Retreinamento ===")
    for strategy in strategies:
        logger.info("\n--- %s ---", strategy.get_strategy_name())

    logger.info("\n=== Retreinamento com novos dados ===")
    rng = np.random.default_rng(RANDOM_STATE)
    idx = rng.integers(0, len(X), 400)
    retrain_model(X[idx], y[idx])


if __name__ == "__main__":
    demo_retraining_strategies()
