"""Pandera Schemas — validacao tipada de DataFrames para ML.

Demonstra como definir schemas Pandera para garantir qualidade e
consistencia dos dados ao longo do pipeline de ML.

Conceitos-chave
---------------
- **DataFrameSchema**: contrato tipado para colunas, tipos e checks.
- **Check**: regra reutilizavel que pode ser composta em colunas e schemas.
- **Validacao lazy**: acumula todos os erros antes de levantar excecao.
- **Coercao de tipos**: Pandera pode converter tipos automaticamente.
- **Schema de entrada vs. schema de saida**: validar tanto dados brutos
  quanto predicoes do modelo.

Referencia:
    Pandera — https://pandera.readthedocs.io/

Requisitos:
    pip install 'pandera[pandas]'

Uso:
    python pandera_schemas.py
"""

import logging
from typing import Any

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42


# ---------------------------------------------------------------------------
# 1. Carregamento seguro do Pandera
# ---------------------------------------------------------------------------


def load_pandera_module():
    """Carrega Pandera de forma compativel com versoes novas e antigas."""
    try:
        import pandera.pandas as pa
        return pa
    except ImportError:
        try:
            import pandera as pa
            return pa
        except ImportError:
            logger.warning("pandera nao instalado. Use: pip install 'pandera[pandas]'")
            return None


# ---------------------------------------------------------------------------
# 2. Schemas de entrada — validar dados brutos
# ---------------------------------------------------------------------------


def create_churn_input_schema():
    """Schema para dados de entrada de churn de telecom.

    Valida colunas criticas, faixas numericas e categorias permitidas.
    Esse schema seria aplicado na ingestao de dados antes de qualquer
    transformacao ou feature engineering.
    """
    pa = load_pandera_module()
    if pa is None:
        return None

    return pa.DataFrameSchema(
        columns={
            "customer_id": pa.Column(
                str,
                checks=[pa.Check.str_length(min_value=1)],
                nullable=False,
                description="Identificador unico do cliente",
            ),
            "tenure": pa.Column(
                int,
                checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(120),
                ],
                nullable=False,
                description="Meses como cliente (0 a 120)",
            ),
            "monthly_charges": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(500),
                ],
                nullable=True,
                description="Cobranca mensal em reais",
            ),
            "total_charges": pa.Column(
                float,
                checks=[pa.Check.greater_than_or_equal_to(0)],
                nullable=True,
                description="Total acumulado de cobrancas",
            ),
            "contract": pa.Column(
                str,
                checks=[pa.Check.isin(["month-to-month", "one_year", "two_year"])],
                nullable=False,
                description="Tipo de contrato",
            ),
            "churn": pa.Column(
                str,
                checks=[pa.Check.isin(["yes", "no"])],
                nullable=False,
                description="Label alvo de churn",
            ),
        },
        checks=[
            pa.Check(
                lambda df: df["monthly_charges"].isna().mean() < 0.05,
                error="Mais de 5% de valores faltantes em monthly_charges",
            ),
            pa.Check(
                lambda df: df["customer_id"].duplicated().sum() == 0,
                error="customer_id possui duplicatas",
            ),
        ],
        coerce=True,
        name="ChurnInputSchema",
        description="Contrato de entrada para dados de churn de telecom",
    )


def create_titanic_schema():
    """Schema para o dataset Titanic (comparacao didatica)."""
    pa = load_pandera_module()
    if pa is None:
        return None

    return pa.DataFrameSchema(
        columns={
            "Survived": pa.Column(int, checks=[pa.Check.isin([0, 1])], nullable=False),
            "Pclass": pa.Column(int, checks=[pa.Check.isin([1, 2, 3])], nullable=False),
            "Age": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(120),
                ],
                nullable=True,
            ),
            "Fare": pa.Column(
                float, checks=[pa.Check.greater_than_or_equal_to(0)], nullable=False,
            ),
            "Sex": pa.Column(str, checks=[pa.Check.isin(["male", "female"])], nullable=False),
        },
        checks=[
            pa.Check(
                lambda df: df["Age"].isna().mean() < 0.3,
                error="Mais de 30% de valores faltantes em Age",
            ),
        ],
        coerce=True,
        name="TitanicSchema",
    )


# ---------------------------------------------------------------------------
# 3. Schemas de saida — validar predicoes
# ---------------------------------------------------------------------------


def create_predictions_schema():
    """Schema para validacao de predicoes de um modelo.

    Validar a saida do modelo e tao importante quanto validar a entrada.
    Predicoes fora de faixa ou com metadados incorretos indicam problemas
    no modelo ou na pipeline de serving.
    """
    pa = load_pandera_module()
    if pa is None:
        return None

    return pa.DataFrameSchema(
        columns={
            "customer_id": pa.Column(str, nullable=False),
            "prediction": pa.Column(int, checks=[pa.Check.isin([0, 1])]),
            "probability": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0.0),
                    pa.Check.less_than_or_equal_to(1.0),
                ],
            ),
            "model_version": pa.Column(str, nullable=False),
        },
        checks=[
            pa.Check(
                lambda df: df["probability"].std() > 0.01,
                error="Probabilidades com variancia muito baixa (modelo degenerado)",
            ),
        ],
        name="PredictionsSchema",
        description="Contrato de saida para predicoes de churn",
    )


# ---------------------------------------------------------------------------
# 4. Datasets sinteticos
# ---------------------------------------------------------------------------


def build_churn_examples(
    random_state: int = RANDOM_STATE,
    rows: int = 100,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera DataFrames validos e invalidos de churn."""
    rng = np.random.default_rng(random_state)

    valid_df = pd.DataFrame({
        "customer_id": [f"C-{i:04d}" for i in range(rows)],
        "tenure": rng.integers(0, 72, size=rows),
        "monthly_charges": rng.normal(65, 20, size=rows).round(2).clip(18, 120).astype(float),
        "total_charges": rng.normal(2000, 800, size=rows).round(2).clip(0, 8000).astype(float),
        "contract": rng.choice(
            ["month-to-month", "one_year", "two_year"], size=rows, p=[0.5, 0.25, 0.25],
        ),
        "churn": rng.choice(["yes", "no"], size=rows, p=[0.27, 0.73]),
    })

    invalid_df = valid_df.copy()
    invalid_df.loc[0, "tenure"] = -5
    invalid_df.loc[1, "monthly_charges"] = 999.99
    invalid_df.loc[2, "total_charges"] = -100.0
    invalid_df.loc[3, "contract"] = "weekly"
    invalid_df.loc[4, "churn"] = "maybe"
    invalid_df.loc[5, "customer_id"] = invalid_df.loc[0, "customer_id"]
    return valid_df, invalid_df


def build_titanic_examples(
    random_state: int = RANDOM_STATE,
    rows: int = 100,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera DataFrames validos e invalidos para Titanic."""
    rng = np.random.default_rng(random_state)
    valid_df = pd.DataFrame({
        "Survived": rng.integers(0, 2, rows),
        "Pclass": rng.integers(1, 4, rows),
        "Age": np.where(rng.random(rows) > 0.2, rng.normal(35, 15, rows).clip(1, 80), np.nan),
        "Fare": rng.exponential(30, rows),
        "Sex": rng.choice(["male", "female"], rows),
    })
    invalid_df = valid_df.copy()
    invalid_df.loc[0, "Survived"] = 5
    invalid_df.loc[1, "Age"] = -5
    invalid_df.loc[2, "Fare"] = -100
    return valid_df, invalid_df


def build_prediction_examples() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera exemplos validos e invalidos de saida de modelo."""
    valid_df = pd.DataFrame({
        "customer_id": ["C-0001", "C-0002", "C-0003", "C-0004", "C-0005"],
        "prediction": [0, 1, 1, 0, 1],
        "probability": [0.12, 0.78, 0.91, 0.35, 0.67],
        "model_version": ["v1.2.0"] * 5,
    })
    invalid_df = valid_df.copy()
    invalid_df.loc[1, "probability"] = 1.8  # fora de [0, 1]
    invalid_df.loc[2, "prediction"] = 3     # fora de {0, 1}
    return valid_df, invalid_df


# ---------------------------------------------------------------------------
# 5. Motor de validacao
# ---------------------------------------------------------------------------


def validate_dataframe(
    df: pd.DataFrame,
    schema_name: str,
) -> dict[str, Any]:
    """Valida um DataFrame contra o schema correspondente.

    Retorna um dicionario com resultado, erros e metadados.
    """
    schema_creators = {
        "churn_input": create_churn_input_schema,
        "titanic": create_titanic_schema,
        "predictions": create_predictions_schema,
    }

    creator = schema_creators.get(schema_name)
    if creator is None:
        return {"schema": schema_name, "valid": False, "error": "Schema desconhecido"}

    schema = creator()
    if schema is None:
        return {"schema": schema_name, "valid": False, "error": "pandera nao disponivel"}

    try:
        schema.validate(df, lazy=True)
        logger.info("[pass] Validacao '%s': %d linhas aprovadas", schema_name, len(df))
        return {"schema": schema_name, "valid": True, "rows": len(df), "errors": []}
    except Exception as exc:
        error_str = str(exc)
        logger.error("[FAIL] Validacao '%s': FALHOU\n%s", schema_name, error_str)
        return {"schema": schema_name, "valid": False, "rows": len(df), "errors": [error_str]}


# ---------------------------------------------------------------------------
# 6. Demo principal
# ---------------------------------------------------------------------------


def run_validation_demo(random_state: int = RANDOM_STATE) -> dict[str, Any]:
    """Executa fluxo completo de validacao com Pandera."""
    pandera_available = load_pandera_module() is not None

    # Churn input
    valid_churn, invalid_churn = build_churn_examples(random_state=random_state)
    # Titanic
    valid_titanic, invalid_titanic = build_titanic_examples(random_state=random_state)
    # Predictions
    valid_pred, invalid_pred = build_prediction_examples()

    results = {
        "pandera_available": pandera_available,
        "churn_valid": validate_dataframe(valid_churn, "churn_input"),
        "churn_invalid": validate_dataframe(invalid_churn, "churn_input"),
        "titanic_valid": validate_dataframe(valid_titanic, "titanic"),
        "titanic_invalid": validate_dataframe(invalid_titanic, "titanic"),
        "predictions_valid": validate_dataframe(valid_pred, "predictions"),
        "predictions_invalid": validate_dataframe(invalid_pred, "predictions"),
    }
    return results


def main() -> None:
    logger.info("=== Pandera Schema Validation Demo ===\n")
    results = run_validation_demo()

    logger.info("\n=== Resumo ===")
    for key, value in results.items():
        if isinstance(value, dict):
            status = "pass" if value.get("valid") else "FAIL"
            logger.info("  [%s] %s", status, key)


if __name__ == "__main__":
    main()
