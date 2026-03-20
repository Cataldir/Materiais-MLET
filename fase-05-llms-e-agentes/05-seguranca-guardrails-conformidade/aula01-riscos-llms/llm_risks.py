from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RiskScenario:
    name: str
    impact: int
    exploitability: int
    control_gap: int


def build_risk_scenarios() -> list[RiskScenario]:
    return [
        RiskScenario("prompt_injection", impact=5, exploitability=5, control_gap=4),
        RiskScenario("pii_leakage", impact=5, exploitability=4, control_gap=4),
        RiskScenario("hallucinated_policy_advice", impact=4, exploitability=3, control_gap=3),
        RiskScenario("tool_misuse", impact=4, exploitability=4, control_gap=3),
    ]


def risk_score(scenario: RiskScenario) -> int:
    return scenario.impact * 3 + scenario.exploitability * 2 + scenario.control_gap


def prioritize_risks() -> list[dict[str, object]]:
    # No GoF pattern applies — simple prioritization over structured threat scenarios.
    ranked = sorted(build_risk_scenarios(), key=risk_score, reverse=True)
    return [
        {
            "name": scenario.name,
            "priority_score": risk_score(scenario),
            "priority": "critical" if risk_score(scenario) >= 27 else "high",
        }
        for scenario in ranked
    ]


def main() -> None:
    print("Taxonomia local de riscos para LLMs\n")
    for risk in prioritize_risks():
        print(f"- {risk['name']}: score={risk['priority_score']} -> {risk['priority']}")


if __name__ == "__main__":
    main()