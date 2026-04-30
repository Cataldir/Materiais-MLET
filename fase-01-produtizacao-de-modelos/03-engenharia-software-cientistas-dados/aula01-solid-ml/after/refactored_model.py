"""REFACTORED: Classificação ML seguindo princípios SOLID.

Versão refatorada de spaghetti_model.py aplicando:
- Single Responsibility Principle (SRP): uma função = uma responsabilidade
- Open/Closed Principle: transformadores extensíveis
- Type hints e documentação completa
- Logging ao invés de print
- Constantes nomeadas ao invés de magic numbers
- Tratamento de erros

Uso:
    python refactored_model.py --data data/titanic.csv --output models/
"""

import logging
import pickle
from pathlib import Path

import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42
TEST_SIZE = 0.2
N_ESTIMATORS = 100
NUMERICAL_FEATURES = ["Age", "Fare", "Pclass", "SibSp", "Parch"]
CATEGORICAL_FEATURES = ["Sex", "Embarked"]
TARGET_COL = "Survived"
FILL_STRATEGIES: dict[str, str | float] = {
    "Age": "mean",
    "Embarked": "S",
    "Fare": "median",
}


def load_data(file_path: Path) -> pd.DataFrame:
    """Carrega e valida o dataset.

    Args:
        file_path: Caminho para o CSV.

    Returns:
        DataFrame carregado.

    Raises:
        FileNotFoundError: Se o arquivo não existir.
        ValueError: Se colunas obrigatórias estiverem faltando.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

    df = pd.read_csv(file_path)
    required_cols = [TARGET_COL] + NUMERICAL_FEATURES + CATEGORICAL_FEATURES
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Colunas faltando: {missing}")

    logger.info("Dataset carregado: %d linhas, %d colunas", len(df), len(df.columns))
    return df


def impute_missing_values(df: pd.DataFrame) -> pd.DataFrame:
    """Imputa valores faltantes conforme estratégias definidas.

    Args:
        df: DataFrame com possíveis valores faltantes.

    Returns:
        DataFrame com valores imputados.
    """
    df = df.copy()
    for col, strategy in FILL_STRATEGIES.items():
        if col not in df.columns:
            continue
        fill_value = (
            getattr(df[col], strategy)() if isinstance(strategy, str) else strategy
        )
        n_missing = df[col].isna().sum()
        df[col] = df[col].fillna(fill_value)
        if n_missing > 0:
            logger.info(
                "Imputados %d valores em '%s' com %s=%s",
                n_missing,
                col,
                strategy,
                fill_value,
            )
    return df


def encode_categoricals(df: pd.DataFrame) -> pd.DataFrame:
    """Codifica variáveis categóricas com LabelEncoder.

    Args:
        df: DataFrame com variáveis categóricas.

    Returns:
        DataFrame com categorias codificadas.
    """
    df = df.copy()
    for col in CATEGORICAL_FEATURES:
        if col not in df.columns:
            continue
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col].astype(str))
    return df


def prepare_features(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Prepara features e target para modelagem.

    Args:
        df: DataFrame processado.

    Returns:
        Tupla (X, y) com features e target.
    """
    feature_cols = [
        c for c in NUMERICAL_FEATURES + CATEGORICAL_FEATURES if c in df.columns
    ]
    X = df[feature_cols]
    y = df[TARGET_COL]
    return X, y


def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    n_estimators: int = N_ESTIMATORS,
) -> RandomForestClassifier:
    """Treina o modelo RandomForest.

    Args:
        X_train: Features de treino.
        y_train: Target de treino.
        n_estimators: Número de árvores.

    Returns:
        Modelo treinado.
    """
    model = RandomForestClassifier(n_estimators=n_estimators, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    logger.info("Modelo treinado com %d árvores", n_estimators)
    return model


def evaluate_model(
    model: RandomForestClassifier,
    X_test: pd.DataFrame,
    y_test: pd.Series,
) -> dict[str, float]:
    """Avalia o modelo e registra métricas.

    Args:
        model: Modelo treinado.
        X_test: Features de teste.
        y_test: Target de teste.

    Returns:
        Dicionário de métricas.
    """
    y_pred = model.predict(X_test)
    y_proba = model.predict_proba(X_test)[:, 1]

    metrics = {
        "accuracy": float((y_pred == y_test).mean()),
        "auc_roc": float(roc_auc_score(y_test, y_proba)),
    }
    logger.info("\n%s", classification_report(y_test, y_pred))
    logger.info("AUC-ROC: %.4f", metrics["auc_roc"])
    return metrics


def save_model(model: RandomForestClassifier, output_dir: Path) -> Path:
    """Serializa e salva o modelo.

    Args:
        model: Modelo treinado.
        output_dir: Diretório de saída.

    Returns:
        Caminho para o arquivo salvo.
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    model_path = output_dir / "titanic_model.pkl"
    with open(model_path, "wb") as f:
        pickle.dump(model, f)
    logger.info("Modelo salvo em: %s", model_path)
    return model_path


def run_pipeline(
    data_path: Path, output_dir: Path = Path("models")
) -> dict[str, float]:
    """Executa o pipeline completo de treino e avaliação.

    Args:
        data_path: Caminho para o CSV de dados.
        output_dir: Diretório para salvar o modelo.

    Returns:
        Métricas de avaliação no conjunto de teste.
    """
    df = load_data(data_path)
    df = impute_missing_values(df)
    df = encode_categoricals(df)
    X, y = prepare_features(df)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE, stratify=y
    )

    model = train_model(X_train, y_train)
    metrics = evaluate_model(model, X_test, y_test)
    save_model(model, output_dir)
    return metrics


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Pipeline de classificação Titanic (refatorado)"
    )
    parser.add_argument("--data", type=Path, default=Path("data/titanic.csv"))
    parser.add_argument("--output", type=Path, default=Path("models"))
    args = parser.parse_args()
    run_pipeline(args.data, args.output)
