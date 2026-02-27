"""Pandera Schemas — validação tipada de DataFrames para ML.

Demonstra como definir schemas Pandera para garantir qualidade
e consistência dos dados ao longo do pipeline de ML.

Requisitos:
    pip install pandera

Uso:
    python pandera_schemas.py
"""

import logging

import numpy as np
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

RANDOM_STATE = 42


def create_titanic_schema():
    """Cria schema Pandera para o dataset Titanic.

    Returns:
        DataFrameSchema para validação do Titanic.
    """
    try:
        import pandera as pa
        from pandera import Column, DataFrameSchema, Check

        return DataFrameSchema(
            columns={
                "Survived": Column(int, checks=[
                    Check.isin([0, 1]),
                ], nullable=False),
                "Pclass": Column(int, checks=[
                    Check.isin([1, 2, 3]),
                ], nullable=False),
                "Age": Column(float, checks=[
                    Check.greater_than_or_equal_to(0),
                    Check.less_than_or_equal_to(120),
                ], nullable=True),
                "Fare": Column(float, checks=[
                    Check.greater_than_or_equal_to(0),
                ], nullable=False),
                "Sex": Column(str, checks=[
                    Check.isin(["male", "female"]),
                ], nullable=False),
            },
            checks=[
                Check(
                    lambda df: df["Age"].isna().mean() < 0.3,
                    error="Mais de 30% de valores faltantes em Age"
                ),
            ],
            coerce=True,
        )
    except ImportError:
        logger.warning("pandera não instalado. pip install pandera")
        return None


def create_predictions_schema():
    """Cria schema para validação de predições de um modelo.

    Returns:
        DataFrameSchema para predições.
    """
    try:
        import pandera as pa
        from pandera import Column, DataFrameSchema, Check

        return DataFrameSchema(
            columns={
                "prediction": Column(int, checks=[
                    Check.isin([0, 1]),
                ]),
                "probability": Column(float, checks=[
                    Check.greater_than_or_equal_to(0.0),
                    Check.less_than_or_equal_to(1.0),
                ]),
                "model_version": Column(str, nullable=False),
            }
        )
    except ImportError:
        return None


def validate_dataframe_with_pandera(df: pd.DataFrame, schema_name: str) -> bool:
    """Valida um DataFrame contra o schema correspondente.

    Args:
        df: DataFrame a validar.
        schema_name: Nome do schema a usar ('titanic' ou 'predictions').

    Returns:
        True se válido, False se houver erros de validação.
    """
    schema_creators = {
        "titanic": create_titanic_schema,
        "predictions": create_predictions_schema,
    }

    schema = schema_creators.get(schema_name, lambda: None)()
    if schema is None:
        logger.error("Schema '%s' não encontrado ou pandera não instalado", schema_name)
        return False

    try:
        schema.validate(df, lazy=True)
        logger.info("✓ Validação '%s': PASSOU (%d linhas)", schema_name, len(df))
        return True
    except Exception as exc:
        logger.error("✗ Validação '%s': FALHOU\n%s", schema_name, exc)
        return False


def demo_pandera_validation() -> None:
    """Demonstra validação com Pandera em dados válidos e inválidos."""
    rng = np.random.default_rng(RANDOM_STATE)

    logger.info("=== Dados Válidos ===")
    valid_df = pd.DataFrame({
        "Survived": rng.integers(0, 2, 100),
        "Pclass": rng.integers(1, 4, 100),
        "Age": np.where(rng.random(100) > 0.2, rng.normal(35, 15, 100).clip(1, 80), np.nan),
        "Fare": rng.exponential(30, 100),
        "Sex": rng.choice(["male", "female"], 100),
    })
    validate_dataframe_with_pandera(valid_df, "titanic")

    logger.info("\n=== Dados Inválidos ===")
    invalid_df = valid_df.copy()
    invalid_df.loc[0, "Survived"] = 5
    invalid_df.loc[1, "Age"] = -5
    invalid_df.loc[2, "Fare"] = -100
    validate_dataframe_with_pandera(invalid_df, "titanic")


if __name__ == "__main__":
    demo_pandera_validation()
