"""Experiment logging — rastreamento de experimentos de ML sem frameworks externos.

Demonstra como registrar hiperparâmetros, métricas e artefatos de forma
sistemática usando apenas Python padrão + CSV.

Uso:
    python experiment_logging.py
"""

import csv
import logging
import time
from pathlib import Path

import numpy as np
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RESULTS_DIR = Path("results")
RANDOM_STATE = 42


class ExperimentTracker:
    """Rastreador simples de experimentos de ML.

    Salva parâmetros e métricas em CSV para análise posterior.

    Attributes:
        experiment_name: Nome do experimento.
        results_path: Caminho para o arquivo de resultados.
        runs: Lista de runs executados.
    """

    def __init__(self, experiment_name: str, results_dir: Path = RESULTS_DIR) -> None:
        """Inicializa o tracker.

        Args:
            experiment_name: Nome do experimento.
            results_dir: Diretório para salvar resultados.
        """
        self.experiment_name = experiment_name
        results_dir.mkdir(parents=True, exist_ok=True)
        self.results_path = results_dir / f"{experiment_name}.csv"
        self.runs: list[dict] = []

    def log_run(self, params: dict, metrics: dict) -> None:
        """Registra uma execução com parâmetros e métricas.

        Args:
            params: Hiperparâmetros do modelo.
            metrics: Métricas de avaliação.
        """
        run = {
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "run_id": len(self.runs) + 1,
            **{f"param_{k}": v for k, v in params.items()},
            **{f"metric_{k}": v for k, v in metrics.items()},
        }
        self.runs.append(run)
        logger.info("Run %d: params=%s | metrics=%s", run["run_id"], params, metrics)

    def save(self) -> None:
        """Salva todos os runs em CSV."""
        if not self.runs:
            logger.warning("Nenhum run para salvar.")
            return
        fieldnames = list(self.runs[0].keys())
        with open(self.results_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.runs)
        logger.info("Resultados salvos em: %s", self.results_path)

    def best_run(self, metric: str) -> dict:
        """Retorna o run com melhor valor para a métrica especificada.

        Args:
            metric: Nome da métrica (prefixo 'metric_' é adicionado automaticamente).

        Returns:
            Dicionário com os dados do melhor run.
        """
        key = f"metric_{metric}" if not metric.startswith("metric_") else metric
        return max(self.runs, key=lambda r: r[key])


def run_hyperparameter_search() -> None:
    """Executa busca de hiperparâmetros com logging de experimentos."""
    X, y = load_iris(return_X_y=True)
    tracker = ExperimentTracker("logistic_regression_iris")

    C_values = [0.001, 0.01, 0.1, 1.0, 10.0, 100.0]
    solvers = ["lbfgs", "liblinear"]

    for C in C_values:
        for solver in solvers:
            model = LogisticRegression(
                C=C, solver=solver, max_iter=1000, random_state=RANDOM_STATE
            )
            scores = cross_val_score(model, X, y, cv=5, scoring="accuracy")
            tracker.log_run(
                params={"C": C, "solver": solver},
                metrics={
                    "cv_accuracy_mean": float(np.mean(scores)),
                    "cv_accuracy_std": float(np.std(scores)),
                },
            )

    tracker.save()
    best = tracker.best_run("cv_accuracy_mean")
    logger.info(
        "\nMelhor run: C=%s, solver=%s → accuracy=%.4f (±%.4f)",
        best["param_C"],
        best["param_solver"],
        best["metric_cv_accuracy_mean"],
        best["metric_cv_accuracy_std"],
    )


if __name__ == "__main__":
    run_hyperparameter_search()
