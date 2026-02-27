"""Transformadores custom reutilizáveis compatíveis com sklearn Pipeline.

Fornece transformadores com fit/transform padronizados para uso em
pipelines sklearn e validação de dados.

Exemplo:
    >>> from ml_utils.transformers import ColumnSelector, OutlierClipper
    >>> pipeline = Pipeline([
    ...     ("select", ColumnSelector(["age", "fare"])),
    ...     ("clip", OutlierClipper()),
    ... ])
"""

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin


class ColumnSelector(BaseEstimator, TransformerMixin):
    """Seleciona colunas específicas de um DataFrame.

    Attributes:
        columns: Lista de colunas a selecionar.
    """

    def __init__(self, columns: list[str]) -> None:
        """Inicializa o seletor de colunas.

        Args:
            columns: Nomes das colunas a manter.
        """
        self.columns = columns

    def fit(self, X: pd.DataFrame, y: pd.Series | None = None) -> "ColumnSelector":
        """Valida que as colunas existem no DataFrame.

        Args:
            X: DataFrame de entrada.
            y: Ignorado.

        Returns:
            Self.

        Raises:
            ValueError: Se alguma coluna não existir.
        """
        missing = [c for c in self.columns if c not in X.columns]
        if missing:
            raise ValueError(f"Colunas não encontradas: {missing}")
        return self

    def transform(self, X: pd.DataFrame, y: pd.Series | None = None) -> pd.DataFrame:
        """Seleciona as colunas especificadas.

        Args:
            X: DataFrame de entrada.
            y: Ignorado.

        Returns:
            DataFrame com apenas as colunas selecionadas.
        """
        return X[self.columns]


class OutlierClipper(BaseEstimator, TransformerMixin):
    """Limita outliers via percentil (compatível com sklearn).

    Attributes:
        lower_percentile: Percentil inferior para clipping.
        upper_percentile: Percentil superior para clipping.
        lower_bounds_: Limites inferiores por feature (após fit).
        upper_bounds_: Limites superiores por feature (após fit).
    """

    def __init__(self, lower_percentile: float = 1.0, upper_percentile: float = 99.0) -> None:
        """Inicializa o clipper.

        Args:
            lower_percentile: Percentil inferior (0-100).
            upper_percentile: Percentil superior (0-100).
        """
        self.lower_percentile = lower_percentile
        self.upper_percentile = upper_percentile
        self.lower_bounds_: np.ndarray | None = None
        self.upper_bounds_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> "OutlierClipper":
        """Calcula limites de clipping.

        Args:
            X: Dados de treino.
            y: Ignorado.

        Returns:
            Self.
        """
        self.lower_bounds_ = np.percentile(X, self.lower_percentile, axis=0)
        self.upper_bounds_ = np.percentile(X, self.upper_percentile, axis=0)
        return self

    def transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Aplica clipping.

        Args:
            X: Dados a transformar.
            y: Ignorado.

        Returns:
            Dados com outliers limitados.

        Raises:
            ValueError: Se o transformer não foi fitado.
        """
        if self.lower_bounds_ is None or self.upper_bounds_ is None:
            raise ValueError("Transformer not fitted yet. Call fit() first.")
        return np.clip(X, self.lower_bounds_, self.upper_bounds_)


class MissingValueImputer(BaseEstimator, TransformerMixin):
    """Imputa valores faltantes com estratégia configurável.

    Attributes:
        strategy: Estratégia de imputação ('mean', 'median', 'constant').
        fill_value: Valor para estratégia 'constant'.
        fill_values_: Valores calculados durante o fit.
    """

    def __init__(self, strategy: str = "mean", fill_value: float = 0.0) -> None:
        """Inicializa o imputer.

        Args:
            strategy: 'mean', 'median', ou 'constant'.
            fill_value: Valor usado quando strategy='constant'.
        """
        self.strategy = strategy
        self.fill_value = fill_value
        self.fill_values_: np.ndarray | None = None

    def fit(self, X: np.ndarray, y: np.ndarray | None = None) -> "MissingValueImputer":
        """Calcula valores de imputação.

        Args:
            X: Dados de treino.
            y: Ignorado.

        Returns:
            Self.
        """
        if self.strategy == "mean":
            self.fill_values_ = np.nanmean(X, axis=0)
        elif self.strategy == "median":
            self.fill_values_ = np.nanmedian(X, axis=0)
        elif self.strategy == "constant":
            self.fill_values_ = np.full(X.shape[1], self.fill_value)
        else:
            raise ValueError(f"Estratégia desconhecida: {self.strategy}")
        return self

    def transform(self, X: np.ndarray, y: np.ndarray | None = None) -> np.ndarray:
        """Imputa valores faltantes.

        Args:
            X: Dados a transformar.
            y: Ignorado.

        Returns:
            Dados com valores imputados.
        """
        if self.fill_values_ is None:
            raise ValueError("Transformer not fitted yet.")
        X_copy = X.copy().astype(float)
        for i, fill_val in enumerate(self.fill_values_):
            mask = np.isnan(X_copy[:, i])
            X_copy[mask, i] = fill_val
        return X_copy
