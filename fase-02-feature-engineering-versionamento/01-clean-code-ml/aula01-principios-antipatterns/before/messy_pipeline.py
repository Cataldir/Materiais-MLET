"""ANTI-PATTERN: Pipeline de feature engineering com problemas de clean code.

Demonstra: god function, magic numbers, sem tratamento de erros,
print em vez de logging, sem type hints.

NÃO use em produção. Veja after/clean_pipeline.py para a versão correta.
"""

import pandas as pd
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler


def run(f):
    # loads data and does everything - god function
    d = pd.read_csv(f)

    # no validation
    d["age"] = d["age"].fillna(d["age"].mean())
    d["income"] = d["income"].fillna(0)

    # magic numbers without explanation
    d = d[d["age"] > 18]
    d = d[d["income"] < 999999]

    # inline encoding
    d["gender"] = (d["gender"] == "M").astype(int)

    X = d[["age", "income", "gender"]]
    y = d["churn"]

    # no train/test split, no cross-validation
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    model = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)
    model.fit(X_scaled, y)

    print("Done! Score:", model.score(X_scaled, y))  # train score, not test!
    return model
