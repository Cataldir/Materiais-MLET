"""Nucleo local do pipeline integrado DVC + tracking."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class PreparedDataset:
    train_rows: int
    test_rows: int


@dataclass(frozen=True, slots=True)
class ModelArtifact:
    threshold: float
    positive_reference: float
    negative_reference: float


@dataclass(frozen=True, slots=True)
class EvaluationReport:
    accuracy: float
    evaluated_rows: int
    tracking_file: str


def read_rows(csv_path: Path) -> list[dict[str, str]]:
    """Le um CSV pequeno em memoria."""

    with csv_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_rows(csv_path: Path, rows: list[dict[str, str]]) -> None:
    """Escreve linhas no mesmo schema da origem."""

    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["customer_id", "monthly_spend", "support_tickets", "late_payments", "churned"]
    with csv_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def score_pressure(row: dict[str, str]) -> float:
    """Transforma sinais operacionais em uma feature simples."""

    return float(row["support_tickets"]) + (2 * float(row["late_payments"]))


def load_params(base_dir: Path) -> dict[str, dict[str, float]]:
    """Carrega parametros do demonstrador a partir de um YAML minimo."""

    params: dict[str, dict[str, float]] = {"prepare": {}, "train": {}}
    current_group = ""
    for raw_line in (base_dir / "params.yaml").read_text(encoding="utf-8").splitlines():
        line = raw_line.rstrip()
        if not line:
            continue
        if not line.startswith("  "):
            current_group = line.replace(":", "")
            params[current_group] = {}
            continue
        key, value = [part.strip() for part in line.split(":", maxsplit=1)]
        params[current_group][key] = float(value)
    return params


def prepare_dataset(base_dir: Path) -> PreparedDataset:
    """Separa treino e teste de forma determinista."""

    params = load_params(base_dir)
    train_rows = int(params["prepare"]["train_rows"])
    rows = read_rows(base_dir / "data" / "raw" / "churn.csv")
    train = rows[:train_rows]
    test = rows[train_rows:]
    write_rows(base_dir / "data" / "processed" / "train.csv", train)
    write_rows(base_dir / "data" / "processed" / "test.csv", test)
    return PreparedDataset(train_rows=len(train), test_rows=len(test))


def train_model(base_dir: Path) -> ModelArtifact:
    """Treina um classificador limiar simples para manter o pack leve."""

    params = load_params(base_dir)
    margin = params["train"]["threshold_margin"]
    rows = read_rows(base_dir / "data" / "processed" / "train.csv")
    positive = [score_pressure(row) for row in rows if row["churned"] == "1"]
    negative = [score_pressure(row) for row in rows if row["churned"] == "0"]
    positive_reference = sum(positive) / len(positive)
    negative_reference = sum(negative) / len(negative)
    model = ModelArtifact(
        threshold=round(((positive_reference + negative_reference) / 2) + margin, 4),
        positive_reference=round(positive_reference, 4),
        negative_reference=round(negative_reference, 4),
    )
    model_path = base_dir / "models" / "model.json"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    model_path.write_text(json.dumps(asdict(model), indent=2), encoding="utf-8")
    return model


def evaluate_model(base_dir: Path) -> EvaluationReport:
    """Avalia o modelo e registra um tracking local em JSON."""

    rows = read_rows(base_dir / "data" / "processed" / "test.csv")
    model = json.loads((base_dir / "models" / "model.json").read_text(encoding="utf-8"))
    threshold = float(model["threshold"])
    hits = 0
    for row in rows:
        prediction = 1 if score_pressure(row) >= threshold else 0
        hits += int(prediction == int(row["churned"]))
    accuracy = round(hits / len(rows), 4)

    metrics_dir = base_dir / "metrics"
    metrics_dir.mkdir(parents=True, exist_ok=True)
    report = {"accuracy": accuracy, "rows": len(rows), "threshold": threshold}
    (metrics_dir / "eval_metrics.json").write_text(
        json.dumps(report, indent=2),
        encoding="utf-8",
    )

    tracking_dir = base_dir / "tracking"
    tracking_dir.mkdir(parents=True, exist_ok=True)
    tracking_file = tracking_dir / "run-001.json"
    tracking_file.write_text(
        json.dumps(
            {
                "params": load_params(base_dir),
                "metrics": report,
                "artifacts": ["models/model.json", "metrics/eval_metrics.json"],
            },
            indent=2,
        ),
        encoding="utf-8",
    )
    return EvaluationReport(
        accuracy=accuracy,
        evaluated_rows=len(rows),
        tracking_file=str(tracking_file.relative_to(base_dir)),
    )


def run_pipeline(base_dir: Path) -> dict[str, object]:
    """Orquestra preparo, treino e avaliacao."""

    prepared = prepare_dataset(base_dir)
    model = train_model(base_dir)
    evaluation = evaluate_model(base_dir)
    return {
        "prepared": asdict(prepared),
        "model": asdict(model),
        "evaluation": asdict(evaluation),
        "stage_status": {"prepare": "ok", "train": "ok", "evaluate": "ok"},
    }