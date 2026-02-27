"""Apache Airflow DAG — pipeline de ML automatizado.

Define um DAG que executa o ciclo completo:
prepare → train → evaluate → deploy

Requisitos:
    pip install apache-airflow

Uso:
    airflow dags test ml_pipeline 2024-01-01
"""

import logging
from datetime import datetime, timedelta
from pathlib import Path

from airflow import DAG
from airflow.operators.python import PythonOperator

logger = logging.getLogger(__name__)

DEFAULT_ARGS = {
    "owner": "ml-team",
    "depends_on_past": False,
    "start_date": datetime(2024, 1, 1),
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}


def task_prepare_data(**context: dict) -> None:
    """Prepara dados: download, limpeza e split treino/teste.

    Args:
        **context: Contexto Airflow com informações do DAG run.
    """
    logger.info("Preparando dados para: %s", context.get("ds"))
    from sklearn.datasets import load_breast_cancer
    from sklearn.model_selection import train_test_split
    import numpy as np

    X, y = load_breast_cancer(return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    data_dir = Path("data/processed")
    data_dir.mkdir(parents=True, exist_ok=True)
    import pandas as pd
    pd.DataFrame(X_train).to_csv(data_dir / "X_train.csv", index=False)
    pd.DataFrame(X_test).to_csv(data_dir / "X_test.csv", index=False)
    pd.Series(y_train).to_csv(data_dir / "y_train.csv", index=False)
    pd.Series(y_test).to_csv(data_dir / "y_test.csv", index=False)
    logger.info("Dados preparados: %d treino, %d teste", len(X_train), len(X_test))


def task_train_model(**context: dict) -> None:
    """Treina modelo com dados preparados.

    Args:
        **context: Contexto Airflow.
    """
    import pandas as pd
    from sklearn.ensemble import RandomForestClassifier
    import pickle

    data_dir = Path("data/processed")
    X_train = pd.read_csv(data_dir / "X_train.csv").values
    y_train = pd.read_csv(data_dir / "y_train.csv").squeeze().values

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    models_dir = Path("models")
    models_dir.mkdir(exist_ok=True)
    with open(models_dir / "model.pkl", "wb") as f:
        pickle.dump(model, f)

    logger.info("Modelo treinado e salvo")


def task_evaluate_model(**context: dict) -> None:
    """Avalia modelo e verifica threshold de qualidade.

    Args:
        **context: Contexto Airflow.

    Raises:
        ValueError: Se AUC-ROC estiver abaixo do threshold mínimo.
    """
    import json
    import pandas as pd
    import pickle
    from sklearn.metrics import roc_auc_score

    data_dir = Path("data/processed")
    X_test = pd.read_csv(data_dir / "X_test.csv").values
    y_test = pd.read_csv(data_dir / "y_test.csv").squeeze().values

    with open("models/model.pkl", "rb") as f:
        model = pickle.load(f)  # noqa: S301

    y_proba = model.predict_proba(X_test)[:, 1]
    auc = float(roc_auc_score(y_test, y_proba))

    metrics = {"auc_roc": auc, "run_date": context.get("ds", "unknown")}
    Path("metrics").mkdir(exist_ok=True)
    with open("metrics/eval_metrics.json", "w") as f:
        json.dump(metrics, f)

    logger.info("AUC-ROC: %.4f", auc)
    if auc < 0.85:
        raise ValueError(f"AUC-ROC {auc:.4f} abaixo do threshold mínimo (0.85)")


def task_deploy_model(**context: dict) -> None:
    """Simula deploy do modelo (substituir por lógica de produção).

    Args:
        **context: Contexto Airflow.
    """
    logger.info("Modelo aprovado. Iniciando deploy...")
    logger.info("Deploy concluído para: %s", context.get("ds"))


with DAG(
    "ml_pipeline",
    default_args=DEFAULT_ARGS,
    description="Pipeline de ML automatizado: prepare → train → evaluate → deploy",
    schedule_interval="@weekly",
    catchup=False,
    tags=["ml", "production"],
) as dag:
    prepare = PythonOperator(task_id="prepare_data", python_callable=task_prepare_data)
    train = PythonOperator(task_id="train_model", python_callable=task_train_model)
    evaluate = PythonOperator(task_id="evaluate_model", python_callable=task_evaluate_model)
    deploy = PythonOperator(task_id="deploy_model", python_callable=task_deploy_model)

    prepare >> train >> evaluate >> deploy
