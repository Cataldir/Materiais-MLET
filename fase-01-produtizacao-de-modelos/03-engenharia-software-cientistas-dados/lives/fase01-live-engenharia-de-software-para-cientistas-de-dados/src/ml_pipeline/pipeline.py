"""Orquestração do pipeline (SRP: amarrar as etapas)."""

import json
import pickle

from sklearn.model_selection import train_test_split

from ml_pipeline.config import PipelineConfig
from ml_pipeline.data import clip_target, load_data
from ml_pipeline.features import add_features
from ml_pipeline.models import train_and_evaluate


def run(config: PipelineConfig) -> dict:
    """Executa o pipeline completo e salva os artefatos."""
    df = load_data()
    df = clip_target(df, config.target_column, config.target_upper_clip)
    df = add_features(df)

    x = df.drop(columns=[config.target_column])
    y = df[config.target_column]
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=config.test_size, random_state=config.random_state
    )

    results = train_and_evaluate(x_train, y_train, x_test, y_test, config.random_state)
    best = results[0]

    config.artifacts_dir.mkdir(parents=True, exist_ok=True)
    with open(config.artifacts_dir / "best_model.pkl", "wb") as f:
        pickle.dump(best["model"], f)
    with open(config.artifacts_dir / "metrics.json", "w") as f:
        json.dump(
            [{k: v for k, v in r.items() if k != "model"} for r in results],
            f,
            indent=2,
        )
    return best
