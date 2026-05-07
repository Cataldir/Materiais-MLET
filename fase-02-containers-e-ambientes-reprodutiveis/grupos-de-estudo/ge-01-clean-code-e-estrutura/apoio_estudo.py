#!/usr/bin/env python3
"""
Script completo de apoio ao grupo de estudo: Grupo de Estudos 1 - Clean Code e Estrutura

O objetivo e transformar discussao em decisao, evidencia e proximo passo.
Usa apenas biblioteca padrao e pode ser executado por qualquer integrante.

No GoF pattern applies - simple educational decision workflow.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

PROFILE = {'topic': 'Grupo de Estudos 1 - Clean Code e Estrutura',
 'phase_label': 'Fase 02',
 'phase_name': 'Containers e Ambientes Reprodutiveis',
 'phase_focus': 'tornar ambiente, dependencias, dados e artefatos reproduziveis entre maquinas '
                'e etapas',
 'tech_goal': 'provar que a solucao pode ser reconstruida, versionada e executada sem depender '
              'da maquina de uma pessoa',
 'decision_options': [{'name': 'Aplicar Grupo de Estudos 1 - Clean Code e Estrutura ao Tech '
                               'Challenge',
                       'impact': 5,
                       'effort': 3,
                       'risk_reduction': 4},
                      {'name': 'Registrar evidencia minima revisavel',
                       'impact': 4,
                       'effort': 2,
                       'risk_reduction': 5},
                      {'name': 'Adiar item sem criterio de aceite',
                       'impact': 1,
                       'effort': 1,
                       'risk_reduction': 0}],
 'evidence_types': ['README atualizado',
                    'script executado',
                    'metrica ou log',
                    'decisao arquitetural',
                    'risco e mitigacao'],
 'references': ['README local: ./README.md',
                'Guia de estudo: ./guia-de-estudo.md',
                'Checklist Tech Challenge: ./checklist-tech-challenge.md',
                'Dockerfile best practices: '
                'https://docs.docker.com/build/building/best-practices/',
                'Kubernetes concepts: https://kubernetes.io/docs/concepts/',
                'MLflow model registry: https://mlflow.org/docs/latest/model-registry.html']}


@dataclass(frozen=True)
class DecisionOption:
    """Opcao de decisao para o Tech Challenge."""

    name: str
    impact: int
    effort: int
    risk_reduction: int


@dataclass(frozen=True)
class RankedDecision:
    """Opcao pontuada para priorizacao."""

    name: str
    impact: int
    effort: int
    risk_reduction: int
    score: int
    evidence: str


def configure_console() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def rank_decision(option: DecisionOption) -> RankedDecision:
    """Pontua decisao favorecendo impacto e reducao de risco."""
    score = option.impact * 2 + option.risk_reduction * 2 - option.effort
    evidence = "documentar antes/depois, comando executado e criterio de aceite"
    return RankedDecision(
        name=option.name,
        impact=option.impact,
        effort=option.effort,
        risk_reduction=option.risk_reduction,
        score=score,
        evidence=evidence,
    )


def build_plan() -> dict:
    """Cria plano de estudo orientado a evidencias."""
    options = [DecisionOption(**item) for item in PROFILE["decision_options"]]
    ranked = sorted((rank_decision(option) for option in options), key=lambda item: item.score, reverse=True)
    return {
        "topic": PROFILE["topic"],
        "phase": PROFILE["phase_label"],
        "focus": PROFILE["phase_focus"],
        "tech_goal": PROFILE["tech_goal"],
        "recommended_decision": asdict(ranked[0]),
        "decision_matrix": [asdict(item) for item in ranked],
        "evidence_types": PROFILE["evidence_types"],
        "references": PROFILE["references"],
    }


def print_plan(plan: dict) -> None:
    """Imprime plano de trabalho para o grupo."""
    print("=" * 78)
    print(f"GRUPO DE ESTUDO: {plan['topic']}")
    print(f"{plan['phase']} - {PROFILE['phase_name']}")
    print("=" * 78)
    print(f"Foco: {plan['focus']}")
    print(f"Objetivo no Tech Challenge: {plan['tech_goal']}")

    print("\nDecisao recomendada para a proxima rodada:")
    decision = plan["recommended_decision"]
    print(f"- {decision['name']}")
    print(f"  Score: {decision['score']}")
    print(f"  Evidencia esperada: {decision['evidence']}")

    print("\nMatriz de decisoes:")
    for item in plan["decision_matrix"]:
        print(f"- score={item['score']} impacto={item['impact']} esforco={item['effort']} risco={item['risk_reduction']} :: {item['name']}")

    print("\nEvidencias aceitas:")
    for evidence in plan["evidence_types"]:
        print(f"- {evidence}")

    print("\nReferencias para seguir sozinho:")
    for reference in plan["references"]:
        print(f"- {reference}")


def run_check() -> int:
    plan = build_plan()
    checks = {
        "topic_defined": bool(plan["topic"]),
        "has_decision_matrix": len(plan["decision_matrix"]) >= 3,
        "has_evidence": len(plan["evidence_types"]) >= 4,
        "has_references": len(plan["references"]) >= 4,
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
    parser.add_argument("--json", action="store_true", help="imprime plano em JSON")
    args = parser.parse_args()

    if args.check:
        return run_check()

    plan = build_plan()
    if args.json:
        print(json.dumps(plan, ensure_ascii=False, indent=2))
    else:
        print_plan(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
