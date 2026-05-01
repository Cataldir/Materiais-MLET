"""Tracking local de um baseline de sumarização textual com MLflow.

Material canônico derivado da branch ``origin/mlflow-bentoml``.
O foco aqui é demonstrar rastreamento de experimento, assinatura de modelo
e logging de artefatos sem depender de pesos externos ou credenciais.
"""

from __future__ import annotations

import logging
import re
from pathlib import Path
from tempfile import TemporaryDirectory

import mlflow
import pandas as pd
from mlflow.models import infer_signature

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)

EXPERIMENT_NAME = "canonical-text-summarization"
DEFAULT_TRACKING_DIR = Path(__file__).resolve().parent / "mlruns"
SUMMARY_SENTENCE_LIMIT = 2

DEMO_ARTICLES = [
    {
        "article": (
            "Uma plataforma de streaming lançou uma curadoria nova para clientes "
            "que abandonaram o carrinho na assinatura premium. A equipe de produto "
            "quer medir se um resumo curto das vantagens do plano aumenta a conversão. "
            "O experimento também precisa registrar tempo de resposta, cobertura das "
            "mensagens e artefatos de exemplo para auditoria de release."
        ),
        "reference_summary": (
            "A empresa quer testar se resumos curtos das vantagens do plano premium "
            "aumentam a conversão e precisam ser auditáveis no pipeline."
        ),
    },
    {
        "article": (
            "Um marketplace educacional prepara uma campanha de retomada de usuários. "
            "Antes de publicar o modelo em produção, o time decidiu comparar execuções "
            "com métricas simples de compressão e sobreposição lexical. O objetivo é "
            "ter uma baseline determinística para validar a infraestrutura de tracking."
        ),
        "reference_summary": (
            "O time quer uma baseline determinística de sumarização para validar a "
            "infraestrutura de tracking antes do deploy em produção."
        ),
    },
    {
        "article": (
            "Uma fintech de crédito está organizando o rollout de um assistente interno "
            "para times de risco. Nesta primeira onda, a exigência não é performance "
            "máxima, mas sim reprodutibilidade, facilidade de depuração e histórico de "
            "métricas para revisão em sala de aula."
        ),
        "reference_summary": (
            "Na primeira onda, a fintech prioriza reprodutibilidade, depuração e "
            "histórico de métricas para ensino."
        ),
    },
]


def split_sentences(text: str) -> list[str]:
    """Segmenta texto em sentenças simples para o baseline rule-based."""
    return [segment.strip() for segment in re.split(r"(?<=[.!?])\s+", text) if segment.strip()]


def summarize_text(text: str, max_sentences: int = SUMMARY_SENTENCE_LIMIT) -> str:
    """Resume o texto mantendo as primeiras sentenças informativas."""
    sentences = split_sentences(text)
    if not sentences:
        return ""
    return " ".join(sentences[:max_sentences])


class RuleBasedSummarizer(mlflow.pyfunc.PythonModel):
    """Modelo MLflow mínimo para demonstrar empacotamento de sumarização."""

    def predict(self, context: object, model_input: pd.DataFrame) -> pd.Series:  # type: ignore[override]
        return model_input["article"].apply(summarize_text)


def build_demo_dataset() -> pd.DataFrame:
    """Cria o dataset demonstrativo usado no tracking."""
    return pd.DataFrame(DEMO_ARTICLES)


def lexical_overlap(prediction: str, reference: str) -> float:
    """Calcula uma sobreposição lexical simples entre previsão e referência."""
    prediction_tokens = {token.lower() for token in re.findall(r"\w+", prediction)}
    reference_tokens = {token.lower() for token in re.findall(r"\w+", reference)}
    if not reference_tokens:
        return 0.0
    return len(prediction_tokens & reference_tokens) / len(reference_tokens)


def evaluate_predictions(predictions: pd.Series, references: pd.Series) -> dict[str, float]:
    """Gera métricas leves para o material de sala."""
    compression_ratios = []
    overlaps = []

    for prediction, reference, article in zip(
        predictions,
        references,
        build_demo_dataset()["article"],
        strict=True,
    ):
        article_word_count = max(len(article.split()), 1)
        compression_ratios.append(len(prediction.split()) / article_word_count)
        overlaps.append(lexical_overlap(prediction, reference))

    return {
        "avg_compression_ratio": float(sum(compression_ratios) / len(compression_ratios)),
        "avg_reference_overlap": float(sum(overlaps) / len(overlaps)),
        "records": float(len(predictions)),
    }


def track_demo_run(tracking_dir: Path = DEFAULT_TRACKING_DIR) -> dict[str, float]:
    """Executa um run completo de tracking com artefatos locais."""
    tracking_dir.mkdir(parents=True, exist_ok=True)
    mlflow.set_tracking_uri(tracking_dir.resolve().as_uri())
    mlflow.set_experiment(EXPERIMENT_NAME)

    dataset = build_demo_dataset()
    model_input = dataset[["article"]]
    predictions = model_input["article"].apply(summarize_text)
    metrics = evaluate_predictions(predictions, dataset["reference_summary"])

    signature = infer_signature(
        model_input=model_input,
        model_output=pd.DataFrame({"summary": predictions}),
    )

    with mlflow.start_run(run_name="rule-based-baseline"):
        mlflow.log_params(
            {
                "max_sentences": SUMMARY_SENTENCE_LIMIT,
                "dataset_size": len(dataset),
                "source_branch": "origin/mlflow-bentoml",
                "canonical_pack": "referencia-mlflow-sumarizacao",
            }
        )
        mlflow.log_metrics(metrics)

        with TemporaryDirectory() as temp_dir:
            preview_path = Path(temp_dir) / "prediction_preview.csv"
            pd.DataFrame(
                {
                    "article": dataset["article"],
                    "reference_summary": dataset["reference_summary"],
                    "predicted_summary": predictions,
                }
            ).to_csv(preview_path, index=False)
            mlflow.log_artifact(str(preview_path), artifact_path="preview")

        mlflow.pyfunc.log_model(
            artifact_path="model",
            python_model=RuleBasedSummarizer(),
            signature=signature,
            input_example=model_input.head(1),
        )

    LOGGER.info("Run registrado em %s", tracking_dir)
    LOGGER.info("Métricas: %s", metrics)
    return metrics


def main() -> None:
    """Executa o exemplo canônico de tracking."""
    track_demo_run()


if __name__ == "__main__":
    main()