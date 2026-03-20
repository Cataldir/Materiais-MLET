"""Fairness Audit — auditoria de viés em modelos de ML.

Demonstra como usar Fairlearn para medir e mitigar viés em modelos,
calculando métricas de equidade por grupo demográfico.

Requisitos:
    pip install fairlearn scikit-learn

Uso:
    python fairness_audit.py
"""

import logging

import numpy as np
import pandas as pd
from sklearn.datasets import fetch_openml
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
SENSITIVE_FEATURE = "sex"


def load_adult_sample() -> tuple[pd.DataFrame, pd.Series, pd.Series]:
    """Carrega amostra do dataset Adult (Census Income).

    Returns:
        Tupla (X, y, sensitive_feature) com features, target e atributo sensível.
    """
    try:
        adult = fetch_openml("adult", version=2, as_frame=True, parser="auto")
        df = adult.data.copy()
        y = (adult.target == ">50K").astype(int)
        df = df.fillna("missing")
        sensitive = df[SENSITIVE_FEATURE].copy()

        cat_cols = df.select_dtypes(include=["category", "object"]).columns
        le = LabelEncoder()
        for col in cat_cols:
            df[col] = le.fit_transform(df[col].astype(str))

        logger.info("Adult dataset: %d amostras", len(df))
        return df, y, sensitive

    except Exception as exc:
        logger.warning(
            "Não foi possível carregar Adult dataset: %s. Usando dados sintéticos.", exc
        )
        rng = np.random.default_rng(RANDOM_STATE)
        n = 500
        df = pd.DataFrame(
            {
                "age": rng.integers(18, 70, n),
                "hours_per_week": rng.integers(20, 80, n),
                "education_num": rng.integers(1, 16, n),
                "sex": rng.integers(0, 2, n),
            }
        )
        sensitive = pd.Series(rng.choice(["Male", "Female"], n), name="sex")
        y = pd.Series(
            (
                df["age"] * 0.5 + df["education_num"] * 2 + rng.normal(0, 10, n) > 40
            ).astype(int)
        )
        return df, y, sensitive


def compute_fairness_metrics(
    y_true: pd.Series | np.ndarray,
    y_pred: np.ndarray,
    sensitive_feature: pd.Series,
) -> pd.DataFrame:
    """Calcula métricas de equidade por grupo demográfico.

    Args:
        y_true: Labels verdadeiros.
        y_pred: Predições do modelo.
        sensitive_feature: Feature sensível (ex: sexo, raça).

    Returns:
        DataFrame com métricas por grupo.
    """
    groups = sensitive_feature.unique()
    results = []
    for group in groups:
        mask = sensitive_feature == group
        group_true = np.array(y_true)[mask]
        group_pred = y_pred[mask]
        accuracy = float((group_pred == group_true).mean())
        positive_rate = float(group_pred.mean())
        results.append(
            {
                "group": group,
                "n": int(mask.sum()),
                "accuracy": accuracy,
                "positive_rate": positive_rate,
            }
        )

    df = pd.DataFrame(results)
    if len(df) >= 2:
        max_rate = df["positive_rate"].max()
        min_rate = df["positive_rate"].min()
        disparate_impact = min_rate / (max_rate + 1e-8)
        logger.info("Disparate Impact Ratio: %.3f (ideal >= 0.8)", disparate_impact)
        if disparate_impact < 0.8:
            logger.warning(
                "⚠️  Possível viés detectado: disparate impact = %.3f", disparate_impact
            )

    return df


def run_fairness_audit() -> None:
    """Executa auditoria completa de fairness em um classificador."""
    X, y, sensitive = load_adult_sample()
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    sensitive_test = (
        sensitive.iloc[X_test.index]
        if hasattr(X_test, "index")
        else sensitive[len(X_train) :]
    )

    model = GradientBoostingClassifier(n_estimators=50, random_state=RANDOM_STATE)
    model.fit(X_train.values, y_train.values)
    y_pred = model.predict(X_test.values)

    logger.info("=== Métricas por Grupo ===")
    metrics_df = compute_fairness_metrics(
        y_test.values, y_pred, sensitive_test.reset_index(drop=True)
    )
    logger.info("\n%s", metrics_df.to_string(index=False))

    try:
        from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate
        from sklearn.metrics import accuracy_score

        mf = MetricFrame(
            metrics={
                "accuracy": accuracy_score,
                "selection_rate": selection_rate,
                "true_positive_rate": true_positive_rate,
            },
            y_true=y_test.values,
            y_pred=y_pred,
            sensitive_features=sensitive_test.reset_index(drop=True),
        )
        logger.info("\n=== Fairlearn MetricFrame ===")
        logger.info(mf.by_group.to_string())
    except ImportError:
        logger.warning("fairlearn não instalado. pip install fairlearn")


if __name__ == "__main__":
    run_fairness_audit()
