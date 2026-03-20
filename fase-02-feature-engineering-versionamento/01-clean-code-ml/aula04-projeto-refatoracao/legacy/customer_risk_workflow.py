"""Workflow legado concentrado em uma unica funcao."""

from __future__ import annotations

from statistics import mean

SAMPLE_RECORDS = [
    {"customer_id": "cust-101", "monthly_spend": 820.0, "tickets": 1, "late": 0},
    {"customer_id": "cust-102", "monthly_spend": 930.0, "tickets": 4, "late": 2},
    {"customer_id": "cust-103", "monthly_spend": 610.0, "tickets": 5, "late": 3},
    {"customer_id": "cust-104", "monthly_spend": 1200.0, "tickets": 1, "late": 0},
]


def run_legacy_workflow(records: list[dict[str, float | int | str]] | None = None) -> dict[str, object]:
    """Resume a carteira sem separar preocupacoes."""

    dataset = records or SAMPLE_RECORDS
    band_counts = {"baixo": 0, "medio": 0, "alto": 0}
    high_risk_ids: list[str] = []
    scores: list[float] = []

    for record in dataset:
        spend = float(record["monthly_spend"]) / 1000.0
        pressure = (int(record["tickets"]) * 0.1) + (int(record["late"]) * 0.15)
        score = round(spend + pressure, 4)
        scores.append(score)

        if score >= 1.45:
            band = "alto"
            high_risk_ids.append(str(record["customer_id"]))
        elif score >= 1.0:
            band = "medio"
        else:
            band = "baixo"

        band_counts[band] += 1

    return {
        "portfolio_health": "watch" if high_risk_ids else "ok",
        "high_risk_ids": high_risk_ids,
        "band_counts": band_counts,
        "mean_score": round(mean(scores), 4),
    }