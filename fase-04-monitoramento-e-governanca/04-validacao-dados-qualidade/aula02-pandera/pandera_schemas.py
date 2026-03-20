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


def create_titanic_schema():
    """Cria schema Pandera para o dataset Titanic.

    Returns:
        DataFrameSchema para validação do Titanic.
    """
    pa = load_pandera_module()
    if pa is None:
        return None

    return pa.DataFrameSchema(
        columns={
            "Survived": pa.Column(
                int,
                checks=[
                    pa.Check.isin([0, 1]),
                ],
                nullable=False,
            ),
            "Pclass": pa.Column(
                int,
                checks=[
                    pa.Check.isin([1, 2, 3]),
                ],
                nullable=False,
            ),
            "Age": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0),
                    pa.Check.less_than_or_equal_to(120),
                ],
                nullable=True,
            ),
            "Fare": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0),
                ],
                nullable=False,
            ),
            "Sex": pa.Column(
                str,
                checks=[
                    pa.Check.isin(["male", "female"]),
                ],
                nullable=False,
            ),
        },
        checks=[
            pa.Check(
                lambda df: df["Age"].isna().mean() < 0.3,
                error="Mais de 30% de valores faltantes em Age",
            ),
        ],
        coerce=True,
    )


def create_predictions_schema():
    """Cria schema para validação de predições de um modelo.

    Returns:
        DataFrameSchema para predições.
    """
    pa = load_pandera_module()
    if pa is None:
        return None

    return pa.DataFrameSchema(
        columns={
            "prediction": pa.Column(
                int,
                checks=[
                    pa.Check.isin([0, 1]),
                ],
            ),
            "probability": pa.Column(
                float,
                checks=[
                    pa.Check.greater_than_or_equal_to(0.0),
                    pa.Check.less_than_or_equal_to(1.0),
                ],
            ),
            "model_version": pa.Column(str, nullable=False),
        }
    )


def build_titanic_examples(
    random_state: int = RANDOM_STATE,
    rows: int = 100,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera DataFrames validos e invalidos para a aula."""
    rng = np.random.default_rng(random_state)
    valid_df = pd.DataFrame(
        {
            "Survived": rng.integers(0, 2, rows),
            "Pclass": rng.integers(1, 4, rows),
            "Age": np.where(
                rng.random(rows) > 0.2, rng.normal(35, 15, rows).clip(1, 80), np.nan
            ),
            "Fare": rng.exponential(30, rows),
            "Sex": rng.choice(["male", "female"], rows),
        }
    )
    invalid_df = valid_df.copy()
    invalid_df.loc[0, "Survived"] = 5
    invalid_df.loc[1, "Age"] = -5
    invalid_df.loc[2, "Fare"] = -100
    return valid_df, invalid_df


def build_prediction_examples() -> tuple[pd.DataFrame, pd.DataFrame]:
    """Gera exemplos validos e invalidos de saida de modelo."""
    valid_df = pd.DataFrame(
        {
            "prediction": [0, 1, 1],
            "probability": [0.12, 0.78, 0.91],
            "model_version": ["v1.0.0", "v1.0.0", "v1.0.0"],
        }
    )
    invalid_df = valid_df.copy()
    invalid_df.loc[1, "probability"] = 1.8
    return valid_df, invalid_df


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


def run_validation_demo(random_state: int = RANDOM_STATE) -> dict[str, bool]:
    """Executa um fluxo enxuto de validacao com fallback amigavel."""
    valid_df, invalid_df = build_titanic_examples(random_state=random_state)
    valid_predictions, invalid_predictions = build_prediction_examples()
    pandera_available = load_pandera_module() is not None

    results = {
        "pandera_available": pandera_available,
        "titanic_valid": validate_dataframe_with_pandera(valid_df, "titanic"),
        "titanic_invalid": validate_dataframe_with_pandera(invalid_df, "titanic"),
        "predictions_valid": validate_dataframe_with_pandera(
            valid_predictions, "predictions"
        ),
        "predictions_invalid": validate_dataframe_with_pandera(
            invalid_predictions, "predictions"
        ),
    }
    return results


def demo_pandera_validation() -> dict[str, bool]:
    """Demonstra validacao com Pandera em dados validos e invalidos."""
    logger.info("=== Dados Válidos ===")
    results = run_validation_demo()
    logger.info("Titanic valido: %s", results["titanic_valid"])
    logger.info("\n=== Dados Inválidos ===")
    logger.info("Titanic invalido: %s", results["titanic_invalid"])
    logger.info("Predictions valido: %s", results["predictions_valid"])
    logger.info("Predictions invalido: %s", results["predictions_invalid"])
    return results


if __name__ == "__main__":
    demo_pandera_validation()
