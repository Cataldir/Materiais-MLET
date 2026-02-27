"""Ensemble comparison — comparação de árvore de decisão, RF, XGBoost e LightGBM.

Inclui benchmark de latência para simular cenários de produção.

Uso:
    python ensemble_comparison.py
"""

import logging
import time

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

try:
    import lightgbm as lgb
    HAS_LIGHTGBM = True
except ImportError:
    HAS_LIGHTGBM = False
    lgb = None

try:
    import xgboost as xgb
    HAS_XGBOOST = True
except ImportError:
    HAS_XGBOOST = False
    xgb = None

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_LATENCY_RUNS = 100


def benchmark_latency(model: object, X_test: np.ndarray) -> float:
    """Mede latência média de inferência (batch único).

    Args:
        model: Modelo treinado com método predict.
        X_test: Dados de teste para medir latência.

    Returns:
        Latência média em milissegundos.
    """
    times = []
    for _ in range(N_LATENCY_RUNS):
        start = time.perf_counter()
        model.predict(X_test[:1])
        times.append((time.perf_counter() - start) * 1000)
    return float(np.mean(times))


def run_comparison() -> pd.DataFrame:
    """Executa comparação entre modelos ensemble.

    Returns:
        DataFrame com métricas de cada modelo.
    """
    cancer = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data, cancer.target,
        test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=cancer.target
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    models: dict[str, object] = {
        "DecisionTree": DecisionTreeClassifier(max_depth=5, random_state=RANDOM_STATE),
        "RandomForest": RandomForestClassifier(n_estimators=100, random_state=RANDOM_STATE),
    }
    if HAS_XGBOOST:
        models["XGBoost"] = xgb.XGBClassifier(
            n_estimators=100, random_state=RANDOM_STATE,
            eval_metric="logloss", verbosity=0
        )
    if HAS_LIGHTGBM:
        models["LightGBM"] = lgb.LGBMClassifier(
            n_estimators=100, random_state=RANDOM_STATE, verbose=-1
        )

    results = []
    for name, model in models.items():
        model.fit(X_train_s, y_train)
        y_pred = model.predict(X_test_s)
        y_proba = model.predict_proba(X_test_s)[:, 1]
        auc = float(roc_auc_score(y_test, y_proba))
        latency_ms = benchmark_latency(model, X_test_s)
        acc = float((y_pred == y_test).mean())

        logger.info("\n--- %s ---", name)
        logger.info(classification_report(y_test, y_pred))
        logger.info("AUC-ROC: %.4f | Latência: %.3fms", auc, latency_ms)

        results.append({
            "model": name,
            "accuracy": acc,
            "auc_roc": auc,
            "latency_ms": latency_ms,
        })

    df = pd.DataFrame(results).sort_values("auc_roc", ascending=False)
    logger.info("\n=== Ranking ===\n%s", df.to_string(index=False))
    return df


if __name__ == "__main__":
    run_comparison()
