"""MLflow tracking — rastreamento de experimentos com MLflow.

Demonstra registro de parâmetros, métricas, artefatos e modelos
no MLflow Tracking Server.

Uso:
    mlflow ui  # Inicia UI em http://localhost:5000
    python mlflow_tracking.py
"""

import logging

import mlflow
import mlflow.sklearn
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

EXPERIMENT_NAME = "breast-cancer-classification"
RANDOM_STATE = 42
TEST_SIZE = 0.2


def run_experiment(
    n_estimators: int,
    max_depth: int | None,
    min_samples_split: int,
) -> dict[str, float]:
    """Executa um experimento e registra no MLflow.

    Args:
        n_estimators: Número de árvores.
        max_depth: Profundidade máxima (None = ilimitada).
        min_samples_split: Mínimo de amostras para split.

    Returns:
        Métricas do experimento.
    """
    cancer = load_breast_cancer()
    X_train, X_test, y_train, y_test = train_test_split(
        cancer.data,
        cancer.target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=cancer.target,
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    with mlflow.start_run():
        mlflow.log_params(
            {
                "n_estimators": n_estimators,
                "max_depth": max_depth,
                "min_samples_split": min_samples_split,
                "random_state": RANDOM_STATE,
                "test_size": TEST_SIZE,
            }
        )

        model = RandomForestClassifier(
            n_estimators=n_estimators,
            max_depth=max_depth,
            min_samples_split=min_samples_split,
            random_state=RANDOM_STATE,
        )
        model.fit(X_train_s, y_train)

        y_pred = model.predict(X_test_s)
        y_proba = model.predict_proba(X_test_s)[:, 1]
        metrics = {
            "accuracy": float((y_pred == y_test).mean()),
            "auc_roc": float(roc_auc_score(y_test, y_proba)),
            "f1_macro": float(f1_score(y_test, y_pred, average="macro")),
        }
        mlflow.log_metrics(metrics)
        mlflow.sklearn.log_model(
            model, "model", registered_model_name="BreastCancerClassifier"
        )

        logger.info("Run registrado: AUC=%.4f", metrics["auc_roc"])
    return metrics


def main() -> None:
    """Executa múltiplos experimentos com diferentes hiperparâmetros."""
    mlflow.set_experiment(EXPERIMENT_NAME)

    experiments = [
        {"n_estimators": 50, "max_depth": 5, "min_samples_split": 2},
        {"n_estimators": 100, "max_depth": 10, "min_samples_split": 5},
        {"n_estimators": 200, "max_depth": None, "min_samples_split": 2},
    ]

    results = []
    for params in experiments:
        logger.info("Executando: %s", params)
        metrics = run_experiment(**params)
        results.append({"params": params, "metrics": metrics})

    best = max(results, key=lambda r: r["metrics"]["auc_roc"])
    logger.info(
        "\nMelhor experimento: %s → AUC=%.4f",
        best["params"],
        best["metrics"]["auc_roc"],
    )
    logger.info("Visualizar resultados: mlflow ui")


if __name__ == "__main__":
    main()
