"""Aula 02 - SRP e refatoracao incremental para scoring de clientes."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

SPEND_NORMALIZER = 1000.0
TICKET_WEIGHT = 0.08
LATE_PAYMENT_WEIGHT = 0.12


@dataclass(frozen=True, slots=True)
class CustomerSnapshot:
    """Representa o estado minimo de um cliente para analise."""

    customer_id: str
    monthly_spend: float
    support_tickets: int
    late_payments: int


@dataclass(frozen=True, slots=True)
class RiskAssessment:
    """Resultado final da avaliacao de risco."""

    customer_id: str
    score: float
    band: str
    actions: list[str]


@dataclass(frozen=True, slots=True)
class RefactorComparison:
    """Compara o comportamento do antes e do depois."""

    legacy: RiskAssessment
    refactored: RiskAssessment
    same_band: bool
    same_actions: bool


def legacy_assess_customer(snapshot: CustomerSnapshot) -> RiskAssessment:
    """Implementacao propositalmente concentrada em uma unica funcao."""

    score = round(
        (snapshot.monthly_spend / SPEND_NORMALIZER)
        + (snapshot.support_tickets * TICKET_WEIGHT)
        + (snapshot.late_payments * LATE_PAYMENT_WEIGHT),
        4,
    )

    if score >= 1.35:
        band = "alto"
        actions = ["acionar-suporte", "revisar-limite"]
    elif score >= 0.95:
        band = "medio"
        actions = ["monitorar", "oferecer-retencao"]
    else:
        band = "baixo"
        actions = ["manter-jornada"]

    return RiskAssessment(
        customer_id=snapshot.customer_id,
        score=score,
        band=band,
        actions=actions,
    )


def normalize_spend(monthly_spend: float) -> float:
    """Extrai a normalizacao para uma funcao dedicada."""

    return monthly_spend / SPEND_NORMALIZER


def calculate_behavior_penalty(snapshot: CustomerSnapshot) -> float:
    """Separa a penalidade comportamental da receita."""

    return (snapshot.support_tickets * TICKET_WEIGHT) + (
        snapshot.late_payments * LATE_PAYMENT_WEIGHT
    )


def calculate_risk_score(snapshot: CustomerSnapshot) -> float:
    """Consolida apenas a formula numerica do score."""

    return round(normalize_spend(snapshot.monthly_spend) + calculate_behavior_penalty(snapshot), 4)


def classify_risk(score: float) -> str:
    """Mapeia score para faixa de risco."""

    if score >= 1.35:
        return "alto"
    if score >= 0.95:
        return "medio"
    return "baixo"


def recommend_actions(band: str) -> list[str]:
    """Define a resposta operacional para cada faixa."""

    actions_by_band = {
        "alto": ["acionar-suporte", "revisar-limite"],
        "medio": ["monitorar", "oferecer-retencao"],
        "baixo": ["manter-jornada"],
    }
    return actions_by_band[band]


def assess_customer(snapshot: CustomerSnapshot) -> RiskAssessment:
    """Versao refatorada com responsabilidades separadas."""

    score = calculate_risk_score(snapshot)
    band = classify_risk(score)
    return RiskAssessment(
        customer_id=snapshot.customer_id,
        score=score,
        band=band,
        actions=recommend_actions(band),
    )


def compare_refactors() -> RefactorComparison:
    """Executa o mesmo caso nas duas abordagens."""

    snapshot = CustomerSnapshot(
        customer_id="cust-002",
        monthly_spend=910.0,
        support_tickets=3,
        late_payments=2,
    )
    legacy = legacy_assess_customer(snapshot)
    refactored = assess_customer(snapshot)
    return RefactorComparison(
        legacy=legacy,
        refactored=refactored,
        same_band=legacy.band == refactored.band,
        same_actions=legacy.actions == refactored.actions,
    )


if __name__ == "__main__":
    print(json.dumps(asdict(compare_refactors()), indent=2, ensure_ascii=False))