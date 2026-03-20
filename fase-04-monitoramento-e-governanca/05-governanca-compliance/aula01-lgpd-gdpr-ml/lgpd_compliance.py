from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DataUseCase:
    name: str
    personal_data: bool
    sensitive_data: bool
    automated_decision: bool
    explicit_consent: bool
    minimization: bool


def build_use_cases() -> list[DataUseCase]:
    return [
        DataUseCase("marketing-segmentation", True, False, False, True, True),
        DataUseCase("credit-auto-rejection", True, False, True, False, False),
        DataUseCase("clinical-triage-support", True, True, False, True, True),
    ]


def classify_use_case(use_case: DataUseCase) -> str:
    # No GoF pattern applies — simple policy assessment over structured cases.
    if use_case.sensitive_data and not use_case.explicit_consent:
        return "block"
    if use_case.automated_decision and not use_case.minimization:
        return "review"
    if use_case.personal_data and not use_case.explicit_consent:
        return "review"
    return "allow"


def evaluate_cases() -> list[dict[str, object]]:
    return [
        {
            "name": use_case.name,
            "status": classify_use_case(use_case),
            "sensitive_data": use_case.sensitive_data,
            "automated_decision": use_case.automated_decision,
        }
        for use_case in build_use_cases()
    ]


def main() -> None:
    print("Enquadramento LGPD/GDPR para casos sinteticos de ML\n")
    for summary in evaluate_cases():
        print(
            f"- {summary['name']}: sensitive={summary['sensitive_data']}, "
            f"automated_decision={summary['automated_decision']} -> {summary['status']}"
        )


if __name__ == "__main__":
    main()