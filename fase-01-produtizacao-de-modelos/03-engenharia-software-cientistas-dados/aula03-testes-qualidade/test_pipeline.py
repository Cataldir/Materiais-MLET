"""Testes de qualidade para pipeline de ML.

Demonstra pytest, pandera para validação de dados e smoke tests.

Uso:
    pytest test_pipeline.py -v
"""

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import load_iris
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

RANDOM_STATE = 42


@pytest.fixture
def iris_data() -> tuple[np.ndarray, np.ndarray]:
    """Fixture que retorna dados Iris divididos em treino/teste."""
    X, y = load_iris(return_X_y=True)
    return train_test_split(X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)


@pytest.fixture
def trained_model(iris_data: tuple) -> RandomForestClassifier:
    """Fixture que treina e retorna um RandomForestClassifier."""
    X_train, _, y_train, _ = iris_data
    model = RandomForestClassifier(n_estimators=10, random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    return model


class TestDataQuality:
    """Testes de qualidade de dados com validações básicas."""

    def test_no_missing_values(self) -> None:
        """Verifica ausência de valores faltantes no Iris."""
        X, _ = load_iris(return_X_y=True)
        df = pd.DataFrame(X)
        assert df.isna().sum().sum() == 0, "Dataset não deve ter valores faltantes"

    def test_feature_ranges(self) -> None:
        """Verifica que features estão dentro de ranges esperados."""
        X, _ = load_iris(return_X_y=True)
        assert np.all(X >= 0), "Features não devem ser negativas"
        assert np.all(X < 10), "Features devem ser menores que 10"

    def test_class_distribution(self) -> None:
        """Verifica distribuição balanceada das classes."""
        _, y = load_iris(return_X_y=True)
        unique, counts = np.unique(y, return_counts=True)
        assert len(unique) == 3, "Deve haver 3 classes"
        assert np.all(counts == 50), "Classes devem ser balanceadas (50 amostras cada)"


class TestModel:
    """Smoke tests e testes de performance do modelo."""

    def test_model_trains_without_error(self, iris_data: tuple) -> None:
        """Verifica que o modelo treina sem erros."""
        X_train, _, y_train, _ = iris_data
        model = RandomForestClassifier(n_estimators=5, random_state=RANDOM_STATE)
        model.fit(X_train, y_train)
        assert hasattr(model, "estimators_")

    def test_model_predicts_correct_shape(
        self, trained_model: RandomForestClassifier, iris_data: tuple
    ) -> None:
        """Verifica shape das predições."""
        _, X_test, _, _ = iris_data
        predictions = trained_model.predict(X_test)
        assert predictions.shape == (len(X_test),)

    def test_model_accuracy_above_threshold(
        self, trained_model: RandomForestClassifier, iris_data: tuple
    ) -> None:
        """Verifica que acurácia mínima é atingida (smoke test de performance)."""
        _, X_test, _, y_test = iris_data
        accuracy = trained_model.score(X_test, y_test)
        assert (
            accuracy >= 0.90
        ), f"Acurácia {accuracy:.2f} abaixo do mínimo esperado (0.90)"

    def test_prediction_probabilities_sum_to_one(
        self, trained_model: RandomForestClassifier, iris_data: tuple
    ) -> None:
        """Verifica que probabilidades somam 1."""
        _, X_test, _, _ = iris_data
        probas = trained_model.predict_proba(X_test)
        sums = probas.sum(axis=1)
        np.testing.assert_allclose(sums, 1.0, atol=1e-6)

    def test_no_nan_in_predictions(
        self, trained_model: RandomForestClassifier, iris_data: tuple
    ) -> None:
        """Verifica ausência de NaN nas predições."""
        _, X_test, _, _ = iris_data
        predictions = trained_model.predict(X_test)
        assert not np.any(np.isnan(predictions.astype(float)))
