"""Caso de negócio canônico para recomendação com features e propensão.

Material derivado da branch ``origin/recommendation-systems``. O script resume
as ideias de popularidade, engenharia de features e priorização comercial em um
único fluxo reproduzível para a fase 02.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)

RANDOM_SEED = 42


@dataclass(frozen=True)
class RecommendationScenarioConfig:
    """Configura o tamanho do cenário sintético."""

    n_products: int = 18
    n_customers: int = 240
    seed: int = RANDOM_SEED


DEFAULT_CONFIG = RecommendationScenarioConfig()


def generate_business_case_frame(
    config: RecommendationScenarioConfig | None = None,
) -> pd.DataFrame:
    """Gera uma base sintética de interação produto-cliente."""
    config = config or DEFAULT_CONFIG
    rng = np.random.default_rng(config.seed)
    rows: list[dict[str, float | int | str]] = []

    for customer_idx in range(config.n_customers):
        customer_segment = ["novo", "recorrente", "vip"][customer_idx % 3]
        segment_multiplier = {"novo": 0.85, "recorrente": 1.0, "vip": 1.15}[customer_segment]

        for product_idx in range(config.n_products):
            impressions = int(rng.integers(20, 150))
            clicks = int(min(impressions, rng.integers(1, 40) * segment_multiplier))
            carts = int(min(clicks, rng.integers(0, 12) * segment_multiplier))
            purchases = int(min(carts, rng.integers(0, 6) * segment_multiplier))
            sentiment = float(np.clip(rng.normal(loc=0.62, scale=0.14), 0.05, 0.99))
            hours_since_last_view = float(rng.integers(1, 168))
            discount_pct = float(rng.choice([0, 5, 10, 15, 20, 25]))
            base_price = float(rng.integers(50, 450))
            margin_pct = float(np.clip(rng.normal(loc=0.28, scale=0.09), 0.05, 0.65))

            propensity_signal = (
                0.8 * (clicks / max(impressions, 1))
                + 1.1 * (carts / max(clicks, 1))
                + 0.7 * sentiment
                + 0.3 * (discount_pct / 25)
                + 0.2 * segment_multiplier
                - 0.15 * (hours_since_last_view / 168)
            )
            purchased_next_cycle = int(propensity_signal > 1.2)

            rows.append(
                {
                    "customer_id": f"C{customer_idx:03d}",
                    "product_id": f"P{product_idx:03d}",
                    "customer_segment": customer_segment,
                    "impressions_7d": impressions,
                    "clicks_7d": clicks,
                    "carts_7d": carts,
                    "purchases_7d": purchases,
                    "sentiment_mean": sentiment,
                    "hours_since_last_view": hours_since_last_view,
                    "discount_pct": discount_pct,
                    "base_price": base_price,
                    "margin_pct": margin_pct,
                    "purchased_next_cycle": purchased_next_cycle,
                }
            )

    return pd.DataFrame(rows)


def engineer_recommendation_features(frame: pd.DataFrame) -> pd.DataFrame:
    """Cria features de negócio para ranking e propensão."""
    features = frame.copy()
    features["ctr_7d"] = features["clicks_7d"] / features["impressions_7d"].clip(lower=1)
    features["cart_rate_7d"] = features["carts_7d"] / features["clicks_7d"].clip(lower=1)
    features["purchase_rate_7d"] = features["purchases_7d"] / features["carts_7d"].clip(lower=1)
    features["value_score"] = features["margin_pct"] * features["base_price"]
    features["freshness_score"] = 1 / (1 + features["hours_since_last_view"])
    features["popularity_score"] = (
        0.45 * features["ctr_7d"]
        + 0.35 * features["sentiment_mean"]
        + 0.20 * features["purchase_rate_7d"]
    )
    return features


def build_propensity_pipeline() -> Pipeline:
    """Monta o pipeline supervisionado para priorização comercial."""
    numeric_features = [
        "impressions_7d",
        "clicks_7d",
        "carts_7d",
        "purchases_7d",
        "sentiment_mean",
        "hours_since_last_view",
        "discount_pct",
        "base_price",
        "margin_pct",
        "ctr_7d",
        "cart_rate_7d",
        "purchase_rate_7d",
        "value_score",
        "freshness_score",
        "popularity_score",
    ]

    preprocessor = ColumnTransformer(
        transformers=[("numeric", StandardScaler(), numeric_features)],
        remainder="drop",
    )

    return Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", LogisticRegression(max_iter=500, random_state=RANDOM_SEED)),
        ]
    )


def rank_recommendations(frame: pd.DataFrame) -> tuple[pd.DataFrame, float]:
    """Treina o modelo e retorna um ranking por produto."""
    features = engineer_recommendation_features(frame)
    feature_matrix = features.drop(
        columns=["purchased_next_cycle", "customer_id", "product_id", "customer_segment"]
    )
    y = features["purchased_next_cycle"]

    x_train, x_test, y_train, y_test, test_index = train_test_split(
        feature_matrix,
        y,
        features.index,
        test_size=0.25,
        random_state=RANDOM_SEED,
        stratify=y,
    )

    pipeline = build_propensity_pipeline()
    pipeline.fit(x_train, y_train)

    test_probabilities = pipeline.predict_proba(x_test)[:, 1]
    auc = float(roc_auc_score(y_test, test_probabilities))

    ranked = features.loc[test_index, ["customer_id", "product_id", "customer_segment", "popularity_score", "value_score"]].copy()
    ranked["propensity_score"] = test_probabilities
    ranked["commercial_priority"] = ranked["propensity_score"] * 0.7 + ranked["popularity_score"] * 0.3
    ranked = ranked.sort_values(by=["commercial_priority", "value_score"], ascending=False)
    return ranked.reset_index(drop=True), auc


def main() -> None:
    """Executa o fluxo completo do caso de negócio."""
    scenario = generate_business_case_frame()
    ranked, auc = rank_recommendations(scenario)
    LOGGER.info("AUC de propensão: %.4f", auc)
    LOGGER.info("Top 10 recomendações:\n%s", ranked.head(10).to_string(index=False))


if __name__ == "__main__":
    main()