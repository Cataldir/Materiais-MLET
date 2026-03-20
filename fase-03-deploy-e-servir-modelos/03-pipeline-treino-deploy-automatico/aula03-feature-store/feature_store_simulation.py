"""Simulacao local de feature store com leitura point-in-time."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Protocol

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class FeatureRecord:
    """Representa uma atualizacao de feature para uma entidade."""

    entity_id: str
    feature_group: str
    event_ts: int
    values: dict[str, float]


@dataclass(frozen=True, slots=True)
class TrainingRow:
    """Linha materializada sem olhar para o futuro."""

    entity_id: str
    reference_ts: int
    features: dict[str, float]


class FeatureRepository(Protocol):
    """Contrato de leitura temporal de features."""

    def get_latest_before(
        self,
        entity_id: str,
        feature_group: str,
        reference_ts: int,
    ) -> FeatureRecord | None:
        """Retorna o registro mais recente anterior ao instante informado."""


class LocalFeatureRepository:
    """Repositorio local em memoria para o registro de features."""

    def __init__(self, records: tuple[FeatureRecord, ...]) -> None:
        self.records = records

    def get_latest_before(
        self,
        entity_id: str,
        feature_group: str,
        reference_ts: int,
    ) -> FeatureRecord | None:
        candidates = [
            record
            for record in self.records
            if record.entity_id == entity_id
            and record.feature_group == feature_group
            and record.event_ts <= reference_ts
        ]
        if not candidates:
            return None
        return max(candidates, key=lambda record: record.event_ts)


def build_demo_repository() -> LocalFeatureRepository:
    """Constroi um conjunto pequeno de registros para o exemplo local."""

    records = (
        FeatureRecord("cust-1", "profile", 1, {"tenure_months": 3.0}),
        FeatureRecord("cust-1", "profile", 6, {"tenure_months": 8.0}),
        FeatureRecord("cust-1", "transactions", 4, {"avg_ticket": 120.0}),
        FeatureRecord("cust-1", "transactions", 8, {"avg_ticket": 150.0}),
        FeatureRecord("cust-2", "profile", 2, {"tenure_months": 12.0}),
        FeatureRecord("cust-2", "transactions", 5, {"avg_ticket": 70.0}),
    )
    return LocalFeatureRepository(records)


def build_point_in_time_dataset() -> tuple[TrainingRow, ...]:
    """Materializa linhas de treino sem leakage temporal."""

    repository = build_demo_repository()
    requests = (("cust-1", 5), ("cust-1", 8), ("cust-2", 6))
    rows: list[TrainingRow] = []
    for entity_id, reference_ts in requests:
        features: dict[str, float] = {}
        for feature_group in ("profile", "transactions"):
            record = repository.get_latest_before(entity_id, feature_group, reference_ts)
            if record is not None:
                features.update(record.values)
        rows.append(
            TrainingRow(
                entity_id=entity_id,
                reference_ts=reference_ts,
                features=features,
            )
        )
    return tuple(rows)


def main() -> None:
    """Executa a materializacao point-in-time e imprime o resultado."""

    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    for row in build_point_in_time_dataset():
        LOGGER.info("%s @ %s -> %s", row.entity_id, row.reference_ts, row.features)


if __name__ == "__main__":
    main()