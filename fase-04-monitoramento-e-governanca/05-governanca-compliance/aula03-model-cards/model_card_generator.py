MODEL_CARD = {
    "nome": "credit-risk-lightgbm",
    "objetivo": "priorizar analise de pedidos de microcredito",
    "dados": "cadastro, historico de pagamento e renda declarada",
    "metrica": "auc=0.84, recall_inadimplencia=0.71",
    "limites": "nao usar como decisao unica para rejeicao automatica",
    "riscos": "sensibilidade a mudanca de perfil regional e a variaveis proxy de renda",
}


def required_sections() -> list[str]:
    """Define as secoes minimas para um model card enxuto."""
    return [
        "## Objetivo",
        "## Dados utilizados",
        "## Metricas principais",
        "## Limites de uso",
        "## Riscos e monitoracao",
    ]


def validate_model_card(card: dict[str, str]) -> dict[str, object]:
    """Valida se os campos essenciais e as secoes minimas estao presentes."""
    rendered = render_card(card)
    missing_fields = [key for key, value in card.items() if not value]
    missing_sections = [section for section in required_sections() if section not in rendered]
    return {
        "valid": not missing_fields and not missing_sections,
        "missing_fields": missing_fields,
        "missing_sections": missing_sections,
    }


def render_card(card: dict[str, str]) -> str:
    sections = [
        f"# Model Card - {card['nome']}",
        "",
        "## Objetivo",
        card["objetivo"],
        "",
        "## Dados utilizados",
        card["dados"],
        "",
        "## Metricas principais",
        card["metrica"],
        "",
        "## Limites de uso",
        card["limites"],
        "",
        "## Riscos e monitoracao",
        card["riscos"],
    ]
    return "\n".join(sections)


def main() -> None:
    print(render_card(MODEL_CARD))


if __name__ == "__main__":
    main()