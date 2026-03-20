from guardrails_demo import apply_guardrails, exercise_prompt_set


def walkthrough(debug: bool = False) -> dict[str, object]:
    prompts_by_level = exercise_prompt_set()
    beginner = apply_guardrails(prompts_by_level["iniciante"])
    if debug:
        breakpoint()

    intermediate = apply_guardrails(prompts_by_level["intermediario"])
    if debug:
        breakpoint()

    advanced = apply_guardrails(prompts_by_level["avancado"])
    if debug:
        breakpoint()

    return {
        "iniciante": beginner,
        "intermediario": intermediate,
        "avancado": advanced,
    }


def main() -> None:
    snapshot = walkthrough(debug=False)
    for level, decisions in snapshot.items():
        print(f"Nivel: {level}")
        for prompt, action, detail in decisions:
            print(f"- {action}: {prompt}")
            print(f"  detalhe: {detail}")


if __name__ == "__main__":
    main()