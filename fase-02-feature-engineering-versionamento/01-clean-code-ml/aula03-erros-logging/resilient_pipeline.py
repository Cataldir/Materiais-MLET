"""Resilient pipeline — tratamento de erros e logging resiliente em ML.

Demonstra patterns de:
- Retry com backoff exponencial
- Fallback para valores seguros
- Logging contextual com extra fields
- Circuit breaker simples

Uso:
    python resilient_pipeline.py
"""

import logging
import time
from collections.abc import Callable
from functools import wraps
from typing import Any, TypeVar

import numpy as np

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

MAX_RETRIES = 3
BACKOFF_BASE = 2.0
RANDOM_STATE = 42

F = TypeVar("F", bound=Callable[..., Any])


def retry_with_backoff(
    max_retries: int = MAX_RETRIES, backoff_base: float = BACKOFF_BASE
) -> Callable[[F], F]:
    """Decorator para retry com backoff exponencial.

    Args:
        max_retries: Número máximo de tentativas.
        backoff_base: Base para cálculo do backoff.

    Returns:
        Decorator configurado.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as exc:
                    wait_time = backoff_base ** (attempt - 1)
                    if attempt == max_retries:
                        logger.error(
                            "Falha após %d tentativas em %s: %s",
                            max_retries,
                            func.__name__,
                            exc,
                        )
                        raise
                    logger.warning(
                        "Tentativa %d/%d falhou em %s. Aguardando %.1fs...",
                        attempt,
                        max_retries,
                        func.__name__,
                        wait_time,
                    )
                    time.sleep(wait_time)
            return None

        return wrapper  # type: ignore[return-value]

    return decorator


def with_fallback(fallback_value: Any) -> Callable[[F], F]:
    """Decorator que retorna valor de fallback em caso de erro.

    Args:
        fallback_value: Valor a retornar em caso de exceção.

    Returns:
        Decorator configurado.
    """

    def decorator(func: F) -> F:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                logger.warning(
                    "Fallback ativado em %s: %s → retornando %s",
                    func.__name__,
                    exc,
                    fallback_value,
                )
                return fallback_value

        return wrapper  # type: ignore[return-value]

    return decorator


class CircuitBreaker:
    """Implementação simples de circuit breaker para chamadas externas.

    Attributes:
        failure_threshold: Número de falhas antes de abrir o circuito.
        recovery_timeout: Tempo em segundos antes de tentar recovery.
        failure_count: Contador de falhas consecutivas.
        last_failure_time: Timestamp da última falha.
        is_open: Estado do circuito.
    """

    def __init__(
        self, failure_threshold: int = 3, recovery_timeout: float = 30.0
    ) -> None:
        """Inicializa o circuit breaker.

        Args:
            failure_threshold: Número de falhas para abrir o circuito.
            recovery_timeout: Segundos antes de tentar recovery.
        """
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time: float = 0.0
        self.is_open = False

    def call(self, func: Callable[[], Any]) -> Any:
        """Executa função com proteção do circuit breaker.

        Args:
            func: Função a executar.

        Returns:
            Resultado da função.

        Raises:
            RuntimeError: Se o circuito estiver aberto.
        """
        if self.is_open:
            elapsed = time.time() - self.last_failure_time
            if elapsed < self.recovery_timeout:
                raise RuntimeError(
                    f"Circuit breaker ABERTO. Recovery em {self.recovery_timeout - elapsed:.0f}s"
                )
            logger.info("Circuit breaker: tentando recovery...")
            self.is_open = False
            self.failure_count = 0

        try:
            result = func()
            self.failure_count = 0
            return result
        except Exception as exc:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.is_open = True
                logger.error(
                    "Circuit breaker ABERTO após %d falhas: %s", self.failure_count, exc
                )
            raise


@with_fallback(fallback_value=np.array([]))
def load_features_with_fallback(path: str) -> np.ndarray:
    """Carrega features com fallback para array vazio em caso de erro.

    Args:
        path: Caminho para o arquivo de features.

    Returns:
        Array de features ou array vazio em caso de erro.
    """
    import json

    with open(path) as f:
        data = json.load(f)
    return np.array(data["features"])


def demo_patterns() -> None:
    """Demonstra os patterns de resiliência implementados."""
    logger.info("=== Demo: Retry com Backoff ===")

    call_count = 0

    @retry_with_backoff(max_retries=3, backoff_base=0.1)
    def flaky_function() -> str:
        nonlocal call_count
        call_count += 1
        if call_count < 3:
            raise ConnectionError(f"Falha temporária #{call_count}")
        return "sucesso!"

    try:
        result = flaky_function()
        logger.info("Resultado: %s (após %d tentativas)", result, call_count)
    except Exception as exc:
        logger.error("Falhou: %s", exc)

    logger.info("\n=== Demo: Fallback ===")
    result_fallback = load_features_with_fallback("/arquivo/inexistente.json")
    logger.info("Fallback result: %s", result_fallback)

    logger.info("\n=== Demo: Circuit Breaker ===")
    cb = CircuitBreaker(failure_threshold=2, recovery_timeout=1.0)

    def always_fails() -> None:
        raise RuntimeError("serviço indisponível")

    for i in range(4):
        try:
            cb.call(always_fails)
        except Exception as exc:
            logger.warning("Chamada %d: %s", i + 1, exc)


if __name__ == "__main__":
    demo_patterns()
