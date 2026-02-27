"""Baseline model — treinamento de modelos heurístico e de regressão logística.

Demonstra como estabelecer baselines sólidas antes de modelos complexos.
Inclui logging de hiperparâmetros e métricas para comparação.

Uso:
    python baseline_model.py
"""

import logging

import numpy as np
import pandas as pd
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2


def load_titanic_data() -> tuple[pd.DataFrame, pd.Series]:
    """Carrega e pré-processa o dataset Titanic.

    Aplica imputação simples e encoding de variáveis categóricas.

    Returns:
        Tupla (X, y) com features e target.
    """
    url = (
        "https://raw.githubusercontent.com/"
        "datasciencedojo/datasets/master/titanic.csv"
    )
    try:
        df = pd.read_csv(url)
        logger.info("Dataset carregado: %d linhas", len(df))
    except Exception:
        logger.warning("Falha ao baixar dados. Usando dados sintéticos.")
        rng = np.random.default_rng(RANDOM_STATE)
        df = pd.DataFrame({
            "Pclass": rng.integers(1, 4, 200),
            "Sex": rng.choice(["male", "female"], 200),
            "Age": rng.normal(30, 15, 200).clip(1, 80),
            "Fare": rng.exponential(30, 200),
            "Survived": rng.integers(0, 2, 200),
        })

    feature_cols = ["Pclass", "Age", "Fare"]
    df = df.dropna(subset=["Survived"])
    df["Age"] = df["Age"].fillna(df["Age"].median())
    df["Fare"] = df["Fare"].fillna(df["Fare"].median())
    if "Sex" in df.columns:
        df["Sex_encoded"] = (df["Sex"] == "female").astype(int)
        feature_cols.append("Sex_encoded")

    X = df[feature_cols]
    y = df["Survived"]
    return X, y


def train_and_evaluate(
    model: Pipeline,
    X_train: pd.DataFrame,
    X_test: pd.DataFrame,
    y_train: pd.Series,
    y_test: pd.Series,
    model_name: str,
) -> dict[str, float]:
    """Treina e avalia um modelo, retornando métricas.

    Args:
        model: Pipeline sklearn a ser treinado.
        X_train: Features de treino.
        X_test: Features de teste.
        y_train: Target de treino.
        y_test: Target de teste.
        model_name: Nome do modelo para logging.

    Returns:
        Dicionário com métricas: accuracy, auc_roc.
    """
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    logger.info("\n--- %s ---", model_name)
    logger.info(classification_report(y_test, y_pred))

    metrics: dict[str, float] = {}
    metrics["accuracy"] = float((y_pred == y_test).mean())

    if hasattr(model, "predict_proba"):
        y_proba = model.predict_proba(X_test)[:, 1]
        metrics["auc_roc"] = float(roc_auc_score(y_test, y_proba))
        logger.info("AUC-ROC: %.4f", metrics["auc_roc"])

    return metrics


def main() -> None:
    """Executa comparação entre baseline heurístico e regressão logística."""
    X, y = load_titanic_data()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    logger.info("Treino: %d | Teste: %d", len(X_train), len(X_test))

    dummy_pipeline = Pipeline([
        ("clf", DummyClassifier(strategy="most_frequent", random_state=RANDOM_STATE)),
    ])
    dummy_metrics = train_and_evaluate(
        dummy_pipeline, X_train, X_test, y_train, y_test, "DummyClassifier (baseline)"
    )

    lr_pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("clf", LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)),
    ])
    lr_metrics = train_and_evaluate(
        lr_pipeline, X_train, X_test, y_train, y_test, "LogisticRegression"
    )

    logger.info("\n=== Comparação ===")
    logger.info(
        "Ganho de acurácia vs baseline: +%.2f%%",
        (lr_metrics["accuracy"] - dummy_metrics["accuracy"]) * 100,
    )


if __name__ == "__main__":
    main()
