from model_card_generator import (
    MODEL_CARD,
    render_card,
    required_sections,
    validate_model_card,
)


def walkthrough(debug: bool = False) -> dict[str, object]:
    raw_card = dict(MODEL_CARD)
    if debug:
        breakpoint()

    sections = required_sections()
    if debug:
        breakpoint()

    rendered = render_card(raw_card)
    validation = validate_model_card(raw_card)
    if debug:
        breakpoint()

    return {
        "raw_card": raw_card,
        "sections": sections,
        "rendered": rendered,
        "validation": validation,
    }


def main() -> None:
    snapshot = walkthrough(debug=False)
    print("Checkpoint 1 - campos de entrada")
    print(sorted(snapshot["raw_card"].keys()))
    print("\nCheckpoint 2 - secoes minimas")
    print(snapshot["sections"])
    print("\nCheckpoint 3 - validacao")
    print(snapshot["validation"])


if __name__ == "__main__":
    main()