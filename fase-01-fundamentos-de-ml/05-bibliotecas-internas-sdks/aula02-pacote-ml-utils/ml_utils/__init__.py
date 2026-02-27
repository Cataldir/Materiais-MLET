"""ml_utils — biblioteca interna de utilitários para ML.

Pacote com transformadores, validadores e helpers reutilizáveis
para pipelines de Machine Learning.

Exemplo:
    >>> from ml_utils.transformers import ColumnSelector, OutlierClipper
    >>> from ml_utils.validators import validate_dataframe
"""

__version__ = "0.1.0"
__all__ = ["transformers", "validators", "metrics"]
