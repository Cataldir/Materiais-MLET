from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class EvaluationCase:
    name: str
    context: str
    reference: str
    answer: str


def build_evaluation_cases() -> list[EvaluationCase]:
    return [
        EvaluationCase(
            "grounded_answer",
            "A politica de cancelamentos exige aviso de 7 dias para reagendamento e 6 horas para substituicao.",
            "Aviso de 7 dias permite reagendamento; com 6 horas, um substituto assume.",
            "Com 7 dias de aviso ha reagendamento; com 6 horas, a operacao busca substituto.",
        ),
        EvaluationCase(
            "partial_answer",
            "A politica de cancelamentos exige aviso de 7 dias para reagendamento e 6 horas para substituicao.",
            "Aviso de 7 dias permite reagendamento; com 6 horas, um substituto assume.",
            "A politica fala em reagendamento quando o aviso e antecipado.",
        ),
        EvaluationCase(
            "hallucinated_answer",
            "A politica de cancelamentos exige aviso de 7 dias para reagendamento e 6 horas para substituicao.",
            "Aviso de 7 dias permite reagendamento; com 6 horas, um substituto assume.",
            "A politica garante cancelamento livre em ate 24 horas e devolucao automatica de custos.",
        ),
    ]


def lexical_overlap(text_a: str, text_b: str) -> float:
    tokens_a = {token.strip('.,;:!?').lower() for token in text_a.split() if token}
    tokens_b = {token.strip('.,;:!?').lower() for token in text_b.split() if token}
    if not tokens_a or not tokens_b:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a | tokens_b)


def evaluate_case(case: EvaluationCase) -> dict[str, object]:
    # Strategy-like evaluation: coverage and grounding act as composable scoring rules.
    grounding = lexical_overlap(case.context, case.answer)
    coverage = lexical_overlap(case.reference, case.answer)
    if grounding < 0.15 or coverage < 0.10:
        decision = "fail"
    elif grounding >= 0.35 and coverage >= 0.30:
        decision = "pass"
    else:
        decision = "warn"
    return {
        "name": case.name,
        "grounding": round(grounding, 3),
        "coverage": round(coverage, 3),
        "decision": decision,
    }


def run_evaluation_demo() -> list[dict[str, object]]:
    return [evaluate_case(case) for case in build_evaluation_cases()]


def main() -> None:
    print("Avaliacao automatizada local para respostas generativas\n")
    for result in run_evaluation_demo():
        print(
            f"- {result['name']}: grounding={result['grounding']:.3f}, "
            f"coverage={result['coverage']:.3f} -> {result['decision']}"
        )


if __name__ == "__main__":
    main()