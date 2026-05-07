#!/usr/bin/env python3
"""
Script completo de follow-up da live: Grupo de Estudos 3 - Avaliacao, Monitoramento e Observabilidade

Transforma a conversa da live em acoes, evidencias e criterio de aceite.
Usa apenas biblioteca padrao e nao depende de notebooks.

No GoF pattern applies - simple educational follow-up workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

PROFILE = {'topic': 'Grupo de Estudos 3 - Avaliacao, Monitoramento e Observabilidade',
 'phase_label': 'Fase 05',
 'phase_name': 'Deploy Avancado de IA Generativa',
 'phase_focus': 'operar aplicacoes generativas com avaliacao, guardrails, observabilidade e '
                'seguranca',
 'actions': [{'name': 'Converter duvida da live em experimento pequeno',
              'priority': 'alta',
              'evidence': 'script, log ou matriz de decisao'},
             {'name': 'Atualizar documentacao publica do projeto',
              'priority': 'alta',
              'evidence': 'link para README ou ADR'},
             {'name': 'Registrar risco que ficou aberto',
              'priority': 'media',
              'evidence': 'item de backlog com criterio de aceite'},
             {'name': 'Preparar demo curta para a proxima revisao',
              'priority': 'media',
              'evidence': 'comando e saida esperada'}],
 'references': ['README local: ./README.md',
                'Follow-up da live: ./follow-up-da-live.md',
                'Guia do grupo: ../guia-de-estudo.md',
                'OWASP Top 10 for LLM Applications: '
                'https://owasp.org/www-project-top-10-for-large-language-model-applications/',
                'OpenAI Evals: https://github.com/openai/evals',
                'LangGraph documentation: https://langchain-ai.github.io/langgraph/']}


@dataclass(frozen=True)
class FollowUpAction:
    """Acao combinada apos a live."""

    name: str
    priority: str
    evidence: str


@dataclass(frozen=True)
class ActionReview:
    """Acao com criterio de aceite."""

    name: str
    priority: str
    evidence: str
    acceptance: str


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def review_action(action: FollowUpAction) -> ActionReview:
    """Acrescenta criterio de aceite para a acao."""
    acceptance = "a evidencia deve ser publica, revisavel e conectada ao Tech Challenge"
    if action.priority == "alta":
        acceptance = "concluir antes da proxima revisao do grupo e registrar link da evidencia"
    return ActionReview(
        name=action.name,
        priority=action.priority,
        evidence=action.evidence,
        acceptance=acceptance,
    )


def build_follow_up() -> dict:
    """Monta follow-up executavel para a live."""
    actions = [FollowUpAction(**item) for item in PROFILE["actions"]]
    reviewed = [review_action(action) for action in actions]
    return {
        "topic": PROFILE["topic"],
        "phase": PROFILE["phase_label"],
        "focus": PROFILE["phase_focus"],
        "actions": [asdict(action) for action in reviewed],
        "references": PROFILE["references"],
    }


def print_follow_up(report: dict) -> None:
    """Imprime follow-up em formato de acao."""
    print("=" * 78)
    print(f"FOLLOW-UP DA LIVE: {report['topic']}")
    print(f"{report['phase']} - {PROFILE['phase_name']}")
    print("=" * 78)
    print(f"Foco: {report['focus']}")

    print("\nAcoes recomendadas:")
    for action in report["actions"]:
        print(f"- [{action['priority'].upper()}] {action['name']}")
        print(f"  Evidencia: {action['evidence']}")
        print(f"  Aceite: {action['acceptance']}")

    print("\nReferencias para seguir sozinho:")
    for reference in report["references"]:
        print(f"- {reference}")


def run_check() -> int:
    report = build_follow_up()
    checks = {
        "topic_defined": bool(report["topic"]),
        "has_actions": len(report["actions"]) >= 3,
        "has_references": len(report["references"]) >= 4,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("[FAIL] " + ", ".join(failed))
        return 1
    print("[OK] script validado")
    return 0


def main() -> int:
    configure_console()
    parser = argparse.ArgumentParser(description=PROFILE["topic"])
    parser.add_argument("--check", action="store_true", help="valida o script rapidamente")
    parser.add_argument("--json", action="store_true", help="imprime follow-up em JSON")
    args = parser.parse_args()

    if args.check:
        return run_check()

    report = build_follow_up()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_follow_up(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
