"""Compara o workflow legado e a versao refatorada."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass

from legacy.customer_risk_workflow import run_legacy_workflow
from refactored.customer_risk_workflow import RiskWorkflowFacade


@dataclass(frozen=True, slots=True)
class ComparisonSnapshot:
    """Resumo da equivalencia observavel entre as versoes."""

    legacy: dict[str, object]
    refactored: dict[str, object]
    same_band_counts: bool
    same_high_risk_ids: bool
    same_portfolio_health: bool


def compare_versions() -> ComparisonSnapshot:
    """Executa as duas implementacoes sobre o mesmo conjunto padrao."""

    legacy = run_legacy_workflow()
    refactored = RiskWorkflowFacade().run()
    return ComparisonSnapshot(
        legacy=legacy,
        refactored=refactored,
        same_band_counts=legacy["band_counts"] == refactored["band_counts"],
        same_high_risk_ids=legacy["high_risk_ids"] == refactored["high_risk_ids"],
        same_portfolio_health=legacy["portfolio_health"] == refactored["portfolio_health"],
    )


if __name__ == "__main__":
    print(json.dumps(asdict(compare_versions()), indent=2, ensure_ascii=False))