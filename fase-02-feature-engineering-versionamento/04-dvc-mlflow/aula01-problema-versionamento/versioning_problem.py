from dataclasses import dataclass


@dataclass(frozen=True)
class ExperimentRun:
    name: str
    dataset_version: str | None
    model_version: str | None
    params_hash: str | None
    metric_auc: float

    def is_reproducible(self) -> bool:
        return all([self.dataset_version, self.model_version, self.params_hash])


RUNS = [
    ExperimentRun("baseline-local", None, None, None, 0.81),
    ExperimentRun("candidate-staging", "dados@2026-03-10", "modelo@1.3.0", "6dd9b1f", 0.84),
    ExperimentRun("incident-review", None, "modelo@1.3.0", None, 0.77),
]


def count_reproducible_runs(runs: list[ExperimentRun] = RUNS) -> int:
    """Conta quantos runs possuem trilha minima para reproducao."""
    return sum(run.is_reproducible() for run in runs)


def main() -> None:
    print("Problema de versionamento em projetos de ML\n")
    for run in RUNS:
        status = "reproduzivel" if run.is_reproducible() else "nao reproduzivel"
        print(
            f"- {run.name}: auc={run.metric_auc:.2f}, "
            f"dataset={run.dataset_version}, modelo={run.model_version}, params={run.params_hash} -> {status}"
        )
    reproducible = count_reproducible_runs()
    print("\nLeitura executiva")
    print(f"- apenas {reproducible} de {len(RUNS)} runs possuem trilha minima de auditoria")
    print("- sem versao de dado e parametros, rollback e comparacao ficam fragilizados")
    print("- DVC e MLflow entram como resposta operacional a esse problema")


if __name__ == "__main__":
    main()