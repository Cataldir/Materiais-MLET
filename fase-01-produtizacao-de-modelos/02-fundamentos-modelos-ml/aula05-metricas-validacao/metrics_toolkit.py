"""Metrics toolkit — conjunto de métricas avançadas para avaliação de modelos.

Inclui PR-AUC, análise custo-benefício e validação robusta com
bootstrap e cross-validation estratificado.

Uso:
    python metrics_toolkit.py
"""

import logging

import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    average_precision_score,
    confusion_matrix,
    f1_score,
    roc_auc_score,
)
from sklearn.model_selection import StratifiedKFold, cross_val_predict

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
N_BOOTSTRAP = 1000
COST_FP = 1.0
COST_FN = 5.0


def pr_auc_score(y_true: np.ndarray, y_proba: np.ndarray) -> float:
    """Calcula a área sob a curva Precision-Recall (PR-AUC).

    Args:
        y_true: Labels verdadeiros.
        y_proba: Probabilidades preditas para a classe positiva.

    Returns:
        PR-AUC score.
    """
    return float(average_precision_score(y_true, y_proba))


def cost_benefit_analysis(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    cost_fp: float = COST_FP,
    cost_fn: float = COST_FN,
    benefit_tp: float = 10.0,
    threshold: float = 0.5,
) -> dict[str, float]:
    """Análise custo-benefício para classificação binária.

    Args:
        y_true: Labels verdadeiros.
        y_proba: Probabilidades preditas.
        cost_fp: Custo de um falso positivo.
        cost_fn: Custo de um falso negativo.
        benefit_tp: Benefício de um verdadeiro positivo.
        threshold: Limiar de classificação.

    Returns:
        Dicionário com TP, FP, FN, TN e valor líquido.
    """
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

    net_value = (tp * benefit_tp) - (fp * cost_fp) - (fn * cost_fn)
    logger.info("Threshold=%.2f: TP=%d, FP=%d, FN=%d, TN=%d", threshold, tp, fp, fn, tn)
    logger.info("Valor líquido: %.2f", net_value)

    return {
        "tp": int(tp),
        "fp": int(fp),
        "fn": int(fn),
        "tn": int(tn),
        "net_value": float(net_value),
    }


def bootstrap_metric(
    y_true: np.ndarray,
    y_proba: np.ndarray,
    n_bootstrap: int = N_BOOTSTRAP,
    confidence: float = 0.95,
) -> dict[str, float]:
    """Estima intervalo de confiança de AUC via bootstrap.

    Args:
        y_true: Labels verdadeiros.
        y_proba: Probabilidades preditas.
        n_bootstrap: Número de amostras bootstrap.
        confidence: Nível de confiança (e.g., 0.95 para 95%).

    Returns:
        Dicionário com AUC médio, std, lower e upper bound.
    """
    rng = np.random.default_rng(RANDOM_STATE)
    aucs = []
    for _ in range(n_bootstrap):
        idx = rng.integers(0, len(y_true), size=len(y_true))
        if len(np.unique(y_true[idx])) < 2:
            continue
        aucs.append(roc_auc_score(y_true[idx], y_proba[idx]))

    alpha = (1 - confidence) / 2
    lower = float(np.percentile(aucs, alpha * 100))
    upper = float(np.percentile(aucs, (1 - alpha) * 100))

    logger.info(
        "Bootstrap AUC: %.4f ± %.4f (IC %.0f%%: [%.4f, %.4f])",
        np.mean(aucs),
        np.std(aucs),
        confidence * 100,
        lower,
        upper,
    )
    return {
        "mean": float(np.mean(aucs)),
        "std": float(np.std(aucs)),
        "lower": lower,
        "upper": upper,
    }


def run_robust_validation() -> None:
    """Executa validação robusta com cross-validation estratificado e bootstrap."""
    cancer = load_breast_cancer()
    X, y = cancer.data, cancer.target

    model = RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE)
    cv = StratifiedKFold(n_splits=10, shuffle=True, random_state=RANDOM_STATE)
    y_proba = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
    y_pred = (y_proba >= 0.5).astype(int)

    logger.info("=== Validação com 10-Fold CV Estratificado ===")
    logger.info("ROC-AUC: %.4f", roc_auc_score(y, y_proba))
    logger.info("PR-AUC:  %.4f", pr_auc_score(y, y_proba))
    logger.info("F1:      %.4f", f1_score(y, y_pred))

    logger.info("\n=== Intervalo de Confiança (Bootstrap) ===")
    bootstrap_metric(y, y_proba)

    logger.info("\n=== Análise Custo-Benefício ===")
    for threshold in [0.3, 0.5, 0.7]:
        cost_benefit_analysis(y, y_proba, threshold=threshold)


if __name__ == "__main__":
    run_robust_validation()
