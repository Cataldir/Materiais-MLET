"""Validacao de payload em runtime com estrategia opcional de Pydantic."""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class PayloadValidationResult:
    """Resultado serializavel de validacao em runtime."""

    payload_name: str
    schema_backend: str
    accepted: bool
    errors: tuple[str, ...]


class SchemaStrategy(Protocol):
    """Contrato para validacao estrutural do payload."""

    name: str

    def validate(self, payload: dict[str, Any]) -> list[str]:
        """Retorna a lista de erros estruturais."""


class LocalSchemaStrategy:
    """Validador estrutural local e deterministico."""

    name = "local"

    def validate(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        required_fields = {"customer_id": str, "age": int, "monthly_spend": (int, float), "prediction_horizon_days": int}
        for field_name, expected_type in required_fields.items():
            if field_name not in payload:
                errors.append(f"missing:{field_name}")
                continue
            if not isinstance(payload[field_name], expected_type):
                errors.append(f"type:{field_name}")
        return errors


class PydanticSchemaStrategy(LocalSchemaStrategy):
    """Usa Pydantic quando disponivel e mantem o mesmo contrato."""

    name = "pydantic"

    def validate(self, payload: dict[str, Any]) -> list[str]:
        from pydantic import BaseModel, ValidationError

        class RuntimePayload(BaseModel):
            customer_id: str
            age: int
            monthly_spend: float
            prediction_horizon_days: int
            segment: str | None = None

        try:
            RuntimePayload(**payload)
        except ValidationError as exc:
            return [f"pydantic:{'.'.join(map(str, error['loc']))}" for error in exc.errors()]
        return []


class ValidationHandler(ABC):
    """Base da Chain of Responsibility da aula."""

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
    """Valida campos de negocio alem do schema basico."""

    def check(self, payload: dict[str, Any]) -> list[str]:
        if not payload.get("customer_id"):
            return ["business:customer_id_empty"]
        return []


class NumericRangeHandler(ValidationHandler):
    """Valida faixas numericas de inferencia."""

    def check(self, payload: dict[str, Any]) -> list[str]:
        errors: list[str] = []
        age = payload.get("age")
        spend = payload.get("monthly_spend")
        horizon = payload.get("prediction_horizon_days")
        if isinstance(age, int) and not 18 <= age <= 100:
            errors.append("range:age")
        if isinstance(spend, (int, float)) and not 0 <= float(spend) <= 10000:
            errors.append("range:monthly_spend")
        if isinstance(horizon, int) and not 1 <= horizon <= 90:
            errors.append("range:prediction_horizon_days")
        return errors


class AllowedSegmentHandler(ValidationHandler):
    """Valida segmentos aceitos pela politica de scoring."""

    def check(self, payload: dict[str, Any]) -> list[str]:
        segment = payload.get("segment")
        if segment is None:
            return []
        if segment not in {"basic", "plus", "vip"}:
            return ["business:segment"]
        return []


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
    first.set_next(NumericRangeHandler()).set_next(AllowedSegmentHandler())
    return first


def build_sample_payloads() -> dict[str, dict[str, Any]]:
    """Gera payloads usados na aula."""

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
    }


def validate_payload(payload_name: str, payload: dict[str, Any]) -> PayloadValidationResult:
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


def run_runtime_validation_demo() -> tuple[PayloadValidationResult, ...]:
    """Executa a validacao dos payloads da aula."""

    return tuple(
        validate_payload(payload_name=name, payload=payload)
        for name, payload in build_sample_payloads().items()
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for result in run_runtime_validation_demo():
        LOGGER.info(
            "%s | backend=%s | accepted=%s | errors=%s",
            result.payload_name,
            result.schema_backend,
            result.accepted,
            list(result.errors),
        )


if __name__ == "__main__":
    main()