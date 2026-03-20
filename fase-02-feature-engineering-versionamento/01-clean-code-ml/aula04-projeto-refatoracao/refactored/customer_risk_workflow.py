"""Workflow refatorado com facade sobre as etapas internas."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import mean

SAMPLE_RECORDS = [
    {"customer_id": "cust-101", "monthly_spend": 820.0, "tickets": 1, "late": 0},
    {"customer_id": "cust-102", "monthly_spend": 930.0, "tickets": 4, "late": 2},
    {"customer_id": "cust-103", "monthly_spend": 610.0, "tickets": 5, "late": 3},
    {"customer_id": "cust-104", "monthly_spend": 1200.0, "tickets": 1, "late": 0},
]


@dataclass(frozen=True, slots=True)
class CustomerRecord:
    customer_id: str
    monthly_spend: float
    tickets: int
    late: int


@dataclass(frozen=True, slots=True)
class RiskResult:
    customer_id: str
    score: float
    band: str


def build_records(records: list[dict[str, float | int | str]] | None = None) -> list[CustomerRecord]:
    """Converte dicionarios em objetos tipados."""

    dataset = records or SAMPLE_RECORDS
    return [
        CustomerRecord(
            customer_id=str(item["customer_id"]),
            monthly_spend=float(item["monthly_spend"]),
            tickets=int(item["tickets"]),
            late=int(item["late"]),
        )
        for item in dataset
    ]


def score_record(record: CustomerRecord) -> RiskResult:
    """Calcula o score e a faixa para um unico registro."""

    score = round((record.monthly_spend / 1000.0) + (record.tickets * 0.1) + (record.late * 0.15), 4)
    if score >= 1.45:
        band = "alto"
    elif score >= 1.0:
        band = "medio"
    else:
        band = "baixo"
    return RiskResult(customer_id=record.customer_id, score=score, band=band)


def summarize_portfolio(results: list[RiskResult]) -> dict[str, object]:
    """Resume o portfolio sem expor detalhes de implementacao interna."""

    band_counts = {"baixo": 0, "medio": 0, "alto": 0}
    for result in results:
        band_counts[result.band] += 1
    high_risk_ids = [result.customer_id for result in results if result.band == "alto"]
    return {
        "portfolio_health": "watch" if high_risk_ids else "ok",
        "high_risk_ids": high_risk_ids,
        "band_counts": band_counts,
        "mean_score": round(mean(result.score for result in results), 4),
    }


class RiskWorkflowFacade:
    """Facade para esconder construcao, scoring e resumo."""

    def run(self, records: list[dict[str, float | int | str]] | None = None) -> dict[str, object]:
        typed_records = build_records(records)
        results = [score_record(record) for record in typed_records]
        return summarize_portfolio(results)