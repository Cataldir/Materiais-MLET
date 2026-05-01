"""Validacao de payload em runtime com estrategia opcional de Pydantic.

Demonstra como proteger fronteiras de sistema (APIs, workers, pipelines)
validando payloads antes de processar inferencia.

Conceitos-chave
---------------
- **Schema Validation**: verificacao estrutural de tipos e campos.
- **Business Rules Validation**: regras de negocio alem do schema.
- **Strategy Pattern**: trocar o backend de validacao sem mudar o contrato.
- **Chain of Responsibility**: compor validadores pequenos e independentes.
- **Pydantic como Strategy opcional**: usa Pydantic quando disponivel,
  fallback local quando nao.

Referencia:
    Pydantic — https://docs.pydantic.dev/

Uso:
    python pydantic_validation.py
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

LOGGER = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# 1. Resultado de validacao
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class PayloadValidationResult:
    """Resultado serializavel de validacao em runtime.

    - ``payload_name``: identificador do payload validado.
    - ``schema_backend``: backend usado (local ou pydantic).
    - ``accepted``: True se nenhum erro foi encontrado.
    - ``errors``: tupla de erros encontrados.
    """

    payload_name: str
    schema_backend: str
    accepted: bool
    errors: tuple[str, ...]


# ---------------------------------------------------------------------------
# 2. Strategy Pattern — backends de validacao
# ---------------------------------------------------------------------------


class SchemaStrategy(Protocol):
    """Contrato para validacao estrutural do payload."""

    name: str

    def validate(self, payload: dict[str, Any]) -> list[str]:
        """Retorna a lista de erros estruturais."""


class LocalSchemaStrategy:
    """Validador estrutural local e deterministico.

    Define os campos obrigatorios e seus tipos esperados.
    Nao depende de nenhuma biblioteca externa.
    """

    name = "local"

    REQUIRED_FIELDS: dict[str, type | tuple[type, ...]] = {
        "customer_id": str,
        "age": int,
        "monthly_spend": (int, float),
        "prediction_horizon_days": int,
    }

    def validate(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for field_name, expected_type in self.REQUIRED_FIELDS.items():
            if field_name not in payload:
                errors.append(f"missing:{field_name}")
                continue
            if not isinstance(payload[field_name], expected_type):
                errors.append(f"type:{field_name}")
        return errors


class PydanticSchemaStrategy(LocalSchemaStrategy):
    """Usa Pydantic quando disponivel e mantem o mesmo contrato.

    Pydantic adiciona coercao automatica de tipos e mensagens de erro
    mais ricas, mas o fallback local garante que o material funciona
    sem a dependencia.
    """

    name = "pydantic"

    def validate(self, payload: dict[str, Any]) -> list[str]:
        from pydantic import BaseModel, Field, ValidationError

        class RuntimePayload(BaseModel):
            customer_id: str = Field(min_length=1)
            age: int = Field(ge=0, le=150)
            monthly_spend: float = Field(ge=0)
            prediction_horizon_days: int = Field(ge=1, le=365)
            segment: str | None = None

        try:
            RuntimePayload(**payload)
        except ValidationError as exc:
            return [
                f"pydantic:{'.'.join(map(str, error['loc']))}"
                for error in exc.errors()
            ]
        return []


# ---------------------------------------------------------------------------
# 3. Chain of Responsibility — validadores de negocio
# ---------------------------------------------------------------------------


class ValidationHandler(ABC):
    """Base da Chain of Responsibility.

    Cada handler executa um check de negocio e delega para o proximo.
    Isso permite adicionar novos checks sem inflar uma unica funcao.
    """

    def __init__(self) -> None:
        self._next: ValidationHandler | None = None

    def set_next(self, handler: ValidationHandler) -> ValidationHandler:
        self._next = handler
        return handler

    def handle(self, payload: dict[str, Any]) -> list[str]:
        errors = self.check(payload)
        if self._next is not None:
            errors.extend(self._next.handle(payload))
        return errors

    @abstractmethod
    def check(self, payload: dict[str, Any]) -> list[str]:
        """Executa um check local."""


class RequiredBusinessFieldsHandler(ValidationHandler):
    """Valida campos de negocio alem do schema basico.

    customer_id vazio e diferente de customer_id ausente — o schema
    aceita a string, mas a regra de negocio exige conteudo.
    """

    def check(self, payload: dict[str, Any]) -> list[str]:
        if not payload.get("customer_id"):
            return ["business:customer_id_empty"]
        return []


class NumericRangeHandler(ValidationHandler):
    """Valida faixas numericas de inferencia.

    Ranges mais apertados que os do schema: representam limites
    operacionais do modelo, nao limites fisicos dos dados.
    """

    RANGES = {
        "age": (18, 100),
        "monthly_spend": (0, 10_000),
        "prediction_horizon_days": (1, 90),
    }

    def check(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        for field, (low, high) in self.RANGES.items():
            value = payload.get(field)
            if isinstance(value, (int, float)) and not low <= float(value) <= high:
                errors.append(f"range:{field}")
        return errors


class AllowedSegmentHandler(ValidationHandler):
    """Valida segmentos aceitos pela politica de scoring."""

    ALLOWED = {"basic", "plus", "vip"}

    def check(self, payload: dict[str, Any]) -> list[str]:
        segment = payload.get("segment")
        if segment is None:
            return []
        if segment not in self.ALLOWED:
            return ["business:segment"]
        return []


class ConsistencyHandler(ValidationHandler):
    """Valida consistencia entre campos relacionados.

    Regras cross-field que nao cabem em validacao por coluna.
    """

    def check(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        spend = payload.get("monthly_spend", 0)
        horizon = payload.get("prediction_horizon_days", 0)
        # Predicoes de horizonte longo com gasto zero sao suspeitas
        if isinstance(horizon, int) and horizon > 60 and isinstance(spend, (int, float)) and spend == 0:
            errors.append("consistency:zero_spend_long_horizon")
        return errors


# ---------------------------------------------------------------------------
# 4. Composicao da pipeline de validacao
# ---------------------------------------------------------------------------


def select_schema_strategy() -> SchemaStrategy:
    """Seleciona o backend estrutural disponivel."""
    try:
        import pydantic  # noqa: F401
    except ImportError:
        return LocalSchemaStrategy()
    return PydanticSchemaStrategy()


def build_validation_chain() -> ValidationHandler:
    """Monta a cadeia de validadores de negocio."""
    first = RequiredBusinessFieldsHandler()
    second = NumericRangeHandler()
    third = AllowedSegmentHandler()
    fourth = ConsistencyHandler()

    first.set_next(second)
    second.set_next(third)
    third.set_next(fourth)
    return first


# ---------------------------------------------------------------------------
# 5. Payloads de exemplo
# ---------------------------------------------------------------------------


def build_sample_payloads() -> dict[str, dict[str, Any]]:
    """Gera payloads usados na aula.

    Cada payload demonstra um cenario diferente:
    - valid: todos os campos corretos
    - range_violation: valores fora da faixa operacional
    - schema_violation: tipos errados e campos invalidos
    - consistency_violation: inconsistencia cross-field
    - missing_fields: campos obrigatorios ausentes
    """
    return {
        "valid_payload": {
            "customer_id": "C-100",
            "age": 41,
            "monthly_spend": 245.8,
            "prediction_horizon_days": 30,
            "segment": "plus",
        },
        "range_violation": {
            "customer_id": "C-101",
            "age": 15,
            "monthly_spend": 120.0,
            "prediction_horizon_days": 120,
            "segment": "basic",
        },
        "schema_violation": {
            "customer_id": "",
            "age": "forty",
            "monthly_spend": -10,
            "prediction_horizon_days": 7,
            "segment": "unknown",
        },
        "consistency_violation": {
            "customer_id": "C-102",
            "age": 30,
            "monthly_spend": 0,
            "prediction_horizon_days": 90,
            "segment": "vip",
        },
        "missing_fields": {
            "customer_id": "C-103",
        },
    }


# ---------------------------------------------------------------------------
# 6. Motor de validacao integrado
# ---------------------------------------------------------------------------


def validate_payload(
    payload_name: str,
    payload: dict[str, Any],
) -> PayloadValidationResult:
    """Executa schema validation e a cadeia de regras locais."""
    schema_strategy = select_schema_strategy()
    chain = build_validation_chain()

    errors = schema_strategy.validate(payload)
    errors.extend(chain.handle(payload))

    normalized_errors = tuple(sorted(dict.fromkeys(errors)))
    return PayloadValidationResult(
        payload_name=payload_name,
        schema_backend=schema_strategy.name,
        accepted=not normalized_errors,
        errors=normalized_errors,
    )


# ---------------------------------------------------------------------------
# 7. Demo principal
# ---------------------------------------------------------------------------


def run_runtime_validation_demo() -> tuple[PayloadValidationResult, ...]:
    """Executa a validacao dos payloads da aula."""
    return tuple(
        validate_payload(payload_name=name, payload=payload)
        for name, payload in build_sample_payloads().items()
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    LOGGER.info("=== Pydantic Runtime Validation Demo ===\n")

    for result in run_runtime_validation_demo():
        status = "pass" if result.accepted else "FAIL"
        LOGGER.info(
            "[%s] %s | backend=%s | errors=%s",
            status,
            result.payload_name,
            result.schema_backend,
            list(result.errors),
        )

    LOGGER.info("\n=== Fim da demo ===")


if __name__ == "__main__":
    main()
