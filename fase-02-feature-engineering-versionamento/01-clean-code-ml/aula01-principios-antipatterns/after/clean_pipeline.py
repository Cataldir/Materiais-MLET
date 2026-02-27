"""CLEAN CODE: Pipeline de feature engineering bem estruturado.

Aplica princípios de clean code:
- Funções pequenas com responsabilidade única (SRP)
- Type hints completos
- Documentação clara
- Logging ao invés de print
- Constantes nomeadas
- Tratamento de erros explícito

Uso:
    python clean_pipeline.py --data data/churn.csv
"""

import argparse
import logging
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MIN_AGE = 18
MAX_INCOME = 500_000
RANDOM_STATE = 42
TEST_SIZE = 0.2
REQUIRED_COLUMNS = ["age", "income", "gender", "churn"]


def validate_input(df: pd.DataFrame) -> None:
    """Valida colunas obrigatórias no DataFrame.

    Args:
        df: DataFrame a validar.

    Raises:
        ValueError: Se colunas obrigatórias estiverem ausentes.
    """
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")
    logger.info("Validação de input: OK (%d colunas, %d linhas)", len(df.columns), len(df))


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa valores faltantes com estratégias por coluna.

    Args:
        df: DataFrame com possíveis valores faltantes.

    Returns:
        DataFrame com valores imputados.
    """
    df = df.copy()
    df["age"] = df["age"].fillna(df["age"].mean())
    df["income"] = df["income"].fillna(0.0)
    n_imputed = df.isna().sum().sum()
    logger.info("Valores imputados: %d", n_imputed)
    return df


def filter_outliers(df: pd.DataFrame) -> pd.DataFrame:
    """Remove outliers com base em regras de negócio documentadas.

    Args:
        df: DataFrame para filtrar.

    Returns:
        DataFrame sem outliers.
    """
    n_before = len(df)
    df = df[(df["age"] >= MIN_AGE) & (df["income"] <= MAX_INCOME)]
    logger.info("Registros removidos por outlier: %d → %d", n_before, len(df))
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Codifica variáveis categóricas.

    Args:
        df: DataFrame com categóricas.

    Returns:
        DataFrame com categóricas codificadas.
    """
    df = df.copy()
    df["gender_encoded"] = (df["gender"] == "M").astype(int)
    return df


def split_features_target(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Separa features e target.

    Args:
        df: DataFrame processado.

    Returns:
        Tupla (X, y).
    """
    feature_cols = ["age", "income", "gender_encoded"]
    return df[feature_cols], df["churn"]


def train_and_evaluate(
    X: pd.DataFrame,
    y: pd.Series,
) -> tuple[GradientBoostingClassifier, dict[str, float]]:
    """Treina e avalia o modelo.

    Args:
        X: Features.
        y: Target.

    Returns:
        Tupla (modelo treinado, métricas).
    """
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )
    scaler = StandardScaler()
    X_train_s = scaler.fit_transform(X_train)
    X_test_s = scaler.transform(X_test)

    model = GradientBoostingClassifier(
        n_estimators=100, learning_rate=0.1, max_depth=3, random_state=RANDOM_STATE
    )
    model.fit(X_train_s, y_train)

    y_proba = model.predict_proba(X_test_s)[:, 1]
    metrics = {"auc_roc": float(roc_auc_score(y_test, y_proba))}
    logger.info("AUC-ROC no teste: %.4f", metrics["auc_roc"])
    return model, metrics


def run_pipeline(data_path: Path) -> dict[str, float]:
    """Executa o pipeline completo de feature engineering + treino.

    Args:
        data_path: Caminho para o CSV de dados.

    Returns:
        Métricas de avaliação.
    """
    if not data_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {data_path}")

    df = pd.read_csv(data_path)
    validate_input(df)
    df = impute_missing_values(df)
    df = filter_outliers(df)
    df = encode_categoricals(df)
    X, y = split_features_target(df)
    _, metrics = train_and_evaluate(X, y)
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=Path("data/churn.csv"))
    args = parser.parse_args()
    run_pipeline(args.data)
