from dataclasses import dataclass


def score_customer(balance: float, tenure: int) -> float:
    return round(0.35 + balance / 10000 - tenure * 0.01, 3)


def validate_row(row: dict[str, float | int]) -> bool:
    return row["balance"] >= 0 and row["tenure"] >= 0


@dataclass(frozen=True)
class CheckResult:
    name: str
    passed: bool
    detail: str


def run_checks() -> list[CheckResult]:
    sample = {"balance": 4200.0, "tenure": 3}
    checks = [
        CheckResult("unit_score_range", 0.0 <= score_customer(4200.0, 3) <= 1.0, "score permanece em faixa valida"),
        CheckResult("unit_negative_tenure", score_customer(1000.0, 0) > score_customer(1000.0, 2), "tenure maior reduz risco estimado"),
        CheckResult("data_contract", validate_row(sample), "linha sintetica respeita contrato minimo"),
    ]
    return checks


def gate_decision(checks: list[CheckResult] | None = None) -> str:
    """Resume o gate como pass ou fail para integracao com CI."""
    evaluated_checks = checks if checks is not None else run_checks()
    return "pass" if all(check.passed for check in evaluated_checks) else "fail"


def main() -> None:
    checks = run_checks()
    print("Gate local de qualidade para CI\n")
    for check in checks:
        status = "PASS" if check.passed else "FAIL"
        print(f"- {status} {check.name}: {check.detail}")
    print("\nDecisao final")
    print("- merge liberado" if gate_decision(checks) == "pass" else "- merge bloqueado")


if __name__ == "__main__":
    main()