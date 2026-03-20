"""Referencia canonica de clustering e PCA para a fase 01.

Uso:
    python unsupervised_clustering_pca.py
"""

from __future__ import annotations

import logging

import pandas as pd
from sklearn.cluster import KMeans
from sklearn.datasets import load_wine
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

LOGGER = logging.getLogger(__name__)
RANDOM_STATE = 42
ENABLE_DEBUG_BREAKPOINT = False


def build_dataset() -> tuple[pd.DataFrame, pd.Series]:
    features, target = load_wine(return_X_y=True, as_frame=True)
    return features, target


def run_reference_demo(debug: bool = False) -> dict[str, object]:
    features, target = build_dataset()

    if debug:
        breakpoint()

    search_rows: list[dict[str, float | int]] = []
    scaled_features = StandardScaler().fit_transform(features)

    for clusters in range(2, 7):
        model = KMeans(n_clusters=clusters, random_state=RANDOM_STATE, n_init=20)
        labels = model.fit_predict(scaled_features)
        search_rows.append(
            {
                "k": clusters,
                "inertia": float(model.inertia_),
                "silhouette": float(silhouette_score(scaled_features, labels)),
            }
        )

    search_frame = pd.DataFrame(search_rows).sort_values("silhouette", ascending=False)
    best_k = int(search_frame.iloc[0]["k"])

    final_model = KMeans(n_clusters=best_k, random_state=RANDOM_STATE, n_init=20)
    cluster_labels = final_model.fit_predict(scaled_features)

    projection = PCA(n_components=2, random_state=RANDOM_STATE).fit(scaled_features)
    components = projection.transform(scaled_features)
    points = pd.DataFrame(
        {
            "pc1": components[:, 0],
            "pc2": components[:, 1],
            "cluster": cluster_labels,
            "target": target,
        }
    )

    return {
        "best_k": best_k,
        "best_silhouette": float(search_frame.iloc[0]["silhouette"]),
        "explained_variance": [float(value) for value in projection.explained_variance_ratio_],
        "cluster_counts": points["cluster"].value_counts().sort_index().to_dict(),
        "search": search_frame.to_dict(orient="records"),
    }


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_reference_demo(debug=ENABLE_DEBUG_BREAKPOINT)
    LOGGER.info("Melhor k: %s", summary["best_k"])
    LOGGER.info("Silhouette: %.3f", summary["best_silhouette"])
    LOGGER.info("Variancia explicada PCA: %s", summary["explained_variance"])


if __name__ == "__main__":
    main()