"""Comparação de regularização — Linear, Ridge, Lasso e Regressão Logística.

Demonstra o impacto do parâmetro de regularização em coeficientes
e performance para problemas de regressão e classificação.

Uso:
    python regularization_comparison.py
"""

import logging

import numpy as np
from sklearn.datasets import fetch_california_housing, load_breast_cancer
from sklearn.linear_model import Lasso, LinearRegression, LogisticRegression, Ridge
from sklearn.metrics import mean_squared_error, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2


def compare_regression_regularization() -> None:
    """Compara LinearRegression, Ridge e Lasso no dataset California Housing."""
    housing = fetch_california_housing()
    X_train, X_test, y_train, y_test = train_test_split(
        housing.data, housing.target, test_size=TEST_SIZE, random_state=RANDOM_STATE
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    alphas = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

    logger.info("\n=== Regressão — Regularização ===")
    lr = LinearRegression()
    lr.fit(X_train_s, y_train)
    rmse = float(np.sqrt(mean_squared_error(y_test, lr.predict(X_test_s))))
    logger.info("LinearRegression: RMSE=%.4f", rmse)

    for alpha in alphas:
        ridge = Ridge(alpha=alpha)
        ridge.fit(X_train_s, y_train)
        rmse_r = float(np.sqrt(mean_squared_error(y_test, ridge.predict(X_test_s))))

        lasso = Lasso(alpha=alpha, max_iter=5000)
        lasso.fit(X_train_s, y_train)
        rmse_l = float(np.sqrt(mean_squared_error(y_test, lasso.predict(X_test_s))))
        n_zero = int(np.sum(lasso.coef_ == 0))

        logger.info(
            "alpha=%.3f → Ridge RMSE=%.4f | Lasso RMSE=%.4f (coefs zerados: %d/%d)",
            alpha,
            rmse_r,
            rmse_l,
            n_zero,
            len(lasso.coef_),
        )


def compare_logistic_regularization() -> None:
    """Compara LogisticRegression com diferentes valores de C (inverso da regularização)."""
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

    C_values = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]

    logger.info("\n=== Regressão Logística — Regularização (C) ===")
    for C in C_values:
        for penalty in ["l1", "l2"]:
            solver = "liblinear" if penalty == "l1" else "lbfgs"
            model = LogisticRegression(
                C=C,
                penalty=penalty,
                solver=solver,
                max_iter=1000,
                random_state=RANDOM_STATE,
            )
            model.fit(X_train_s, y_train)
            auc = float(roc_auc_score(y_test, model.predict_proba(X_test_s)[:, 1]))
            n_zero = int(np.sum(model.coef_ == 0))
            logger.info(
                "C=%.3f, penalty=%s → AUC=%.4f (coefs zerados: %d)",
                C,
                penalty,
                auc,
                n_zero,
            )


if __name__ == "__main__":
    compare_regression_regularization()
    compare_logistic_regularization()
