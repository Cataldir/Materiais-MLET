"""Testes para a API de inferência usando TestClient.

Demonstra como testar endpoints FastAPI sem servidor HTTP.

Uso:
    pytest test_api.py -v
"""

import pytest
from api import app
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client() -> TestClient:
    """Cria TestClient para a aplicação FastAPI."""
    return TestClient(app)


class TestHealthEndpoints:
    """Testes para endpoints de saúde."""

    def test_health_returns_ok(self, client: TestClient) -> None:
        """Verifica que /health retorna 200 e status ok."""
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json()["status"] == "ok"

    def test_ready_returns_ready(self, client: TestClient) -> None:
        """Verifica que /ready retorna 200 quando modelo está carregado."""
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.json()["status"] == "ready"


class TestPredictEndpoint:
    """Testes para o endpoint /predict."""

    VALID_SETOSA = {
        "sepal_length": 5.1,
        "sepal_width": 3.5,
        "petal_length": 1.4,
        "petal_width": 0.2,
    }

    def test_predict_returns_valid_class(self, client: TestClient) -> None:
        """Verifica que /predict retorna classe válida."""
        response = client.post("/predict", json=self.VALID_SETOSA)
        assert response.status_code == 200
        data = response.json()
        assert data["predicted_class"] in [0, 1, 2]
        assert data["predicted_label"] in ["setosa", "versicolor", "virginica"]

    def test_predict_probabilities_sum_to_one(self, client: TestClient) -> None:
        """Verifica que probabilidades somam aproximadamente 1."""
        response = client.post("/predict", json=self.VALID_SETOSA)
        assert response.status_code == 200
        probs = response.json()["probabilities"]
        total = sum(probs.values())
        assert abs(total - 1.0) < 1e-6

    def test_predict_invalid_feature_value(self, client: TestClient) -> None:
        """Verifica que features inválidas retornam 422."""
        invalid = {**self.VALID_SETOSA, "sepal_length": -1.0}
        response = client.post("/predict", json=invalid)
        assert response.status_code == 422

    def test_predict_missing_field(self, client: TestClient) -> None:
        """Verifica que campos faltando retornam 422."""
        incomplete = {"sepal_length": 5.1, "sepal_width": 3.5}
        response = client.post("/predict", json=incomplete)
        assert response.status_code == 422

    def test_predict_latency_is_positive(self, client: TestClient) -> None:
        """Verifica que latência reportada é positiva."""
        response = client.post("/predict", json=self.VALID_SETOSA)
        assert response.status_code == 200
        assert response.json()["latency_ms"] > 0
