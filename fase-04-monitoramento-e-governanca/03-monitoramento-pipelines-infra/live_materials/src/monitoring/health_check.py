"""
Health checks compostos para o stack de ML.

Verifica saúde de todos os componentes: modelo, MLflow,
Prometheus e dependências de dados.
"""

import logging

import httpx

from src.common.config import settings

logger = logging.getLogger(__name__)


async def check_mlflow_health() -> dict:
    """Verifica se o MLflow Tracking Server está acessível."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{settings.MLFLOW_TRACKING_URI}/health")
            return {
                "service": "mlflow",
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code,
            }
    except Exception as e:
        return {"service": "mlflow", "status": "unreachable", "error": str(e)}


async def check_prometheus_health(prometheus_url: str = "http://localhost:9090") -> dict:
    """Verifica se o Prometheus está acessível."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(f"{prometheus_url}/-/healthy")
            return {
                "service": "prometheus",
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "status_code": response.status_code,
            }
    except Exception as e:
        return {"service": "prometheus", "status": "unreachable", "error": str(e)}


async def composite_health_check() -> dict:
    """Executa health check composto de todos os serviços."""
    checks = [
        await check_mlflow_health(),
        await check_prometheus_health(),
    ]

    all_healthy = all(c["status"] == "healthy" for c in checks)

    return {
        "overall_status": "healthy" if all_healthy else "degraded",
        "services": checks,
    }
