#!/usr/bin/env python3
"""
Script completo de apoio a live: Latencia e Performance em Dados Nao Estruturados

Este material e um exercicio executavel de engenharia de machine learning.
Ele usa apenas biblioteca padrao, gera um relatorio de gates tecnicos e aponta
referencias para estudo independente.

No GoF pattern applies - simple educational data transform with small functions.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass
from statistics import mean

PROFILE = {'topic': 'Latencia e Performance em Dados Nao Estruturados',
 'phase_label': 'Fase 03',
 'phase_name': 'Cloud e MLOps',
 'phase_focus': 'automatizar entrega, observabilidade, rollback e desempenho operacional em '
                'ambiente de nuvem',
 'scenario': 'monitoracao de performance',
 'concepts': ['SLO', 'drift', 'observability'],
 'risks': ['otimizacao que reduz qualidade', 'SLO sem medicao', 'alerta sem acao'],
 'steps': ['Separar metrica tecnica, metrica de modelo e metrica de negocio.',
           'Definir alerta que indique acao e responsavel.',
           'Descrever decisao quando o alerta dispara.'],
 'gates': [{'name': 'latencia_p95',
            'value': 0.82,
            'threshold': 0.75,
            'evidence': 'latencia atende ao limite'},
           {'name': 'erro_5xx',
            'value': 0.98,
            'threshold': 0.97,
            'evidence': 'taxa de erro fica no orcamento'},
           {'name': 'drift_modelo',
            'value': 0.71,
            'threshold': 0.7,
            'evidence': 'mudanca de distribuicao esta sob observacao'},
           {'name': 'alerta_acionavel',
            'value': 0.84,
            'threshold': 0.8,
            'evidence': 'alerta aponta acao concreta'}],
 'references': ['README local: ./README.md',
                'Guia da live: ./guia-da-live.md',
                'Google Cloud MLOps guide: '
                'https://cloud.google.com/architecture/mlops-continuous-delivery-and-automation-pipelines-in-machine-learning',
                'Azure Architecture Center - MLOps: '
                'https://learn.microsoft.com/azure/architecture/example-scenario/mlops/mlops-technical-paper',
                'OpenTelemetry documentation: https://opentelemetry.io/docs/']}


@dataclass(frozen=True)
class Gate:
    """Representa um criterio mensuravel de engenharia."""

    name: str
    value: float
    threshold: float
    evidence: str


@dataclass(frozen=True)
class GateResult:
    """Resultado calculado para um gate tecnico."""

    name: str
    value: float
    threshold: float
    passed: bool
    evidence: str
    recommendation: str


def configure_console() -> None:
    """Forca UTF-8 quando o terminal Python permitir."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")


def build_gates() -> list[Gate]:
    """Cria gates a partir do perfil tematico da live."""
    return [Gate(**item) for item in PROFILE["gates"]]


def evaluate_gate(gate: Gate) -> GateResult:
    """Avalia um gate considerando se metrica maior ou igual e melhor."""
    passed = gate.value >= gate.threshold
    if passed:
        recommendation = "manter evidencia e explicar criterio de aceite"
    else:
        recommendation = "melhorar implementacao antes de promover a entrega"
    return GateResult(
        name=gate.name,
        value=gate.value,
        threshold=gate.threshold,
        passed=passed,
        evidence=gate.evidence,
        recommendation=recommendation,
    )


def readiness_score(results: list[GateResult]) -> float:
    """Calcula prontidao combinando cobertura e margem dos gates."""
    if not results:
        return 0.0
    ratios = [min(result.value / result.threshold, 1.25) for result in results if result.threshold > 0]
    return round(mean(ratios) * 80, 2)


def build_report() -> dict:
    """Monta um relatorio autocontido para estudo e discussao."""
    results = [evaluate_gate(gate) for gate in build_gates()]
    return {
        "topic": PROFILE["topic"],
        "phase": PROFILE["phase_label"],
        "scenario": PROFILE["scenario"],
        "focus": PROFILE["phase_focus"],
        "readiness_score": readiness_score(results),
        "passed": all(result.passed for result in results),
        "concepts": PROFILE["concepts"],
        "risks": PROFILE["risks"],
        "steps": PROFILE["steps"],
        "gates": [asdict(result) for result in results],
        "references": PROFILE["references"],
    }


def print_report(report: dict) -> None:
    """Imprime o relatorio em formato amigavel para a live."""
    print("=" * 78)
    print(f"LIVE: {report['topic']}")
    print(f"{report['phase']} - {PROFILE['phase_name']}")
    print(f"Cenario: {report['scenario']}")
    print("=" * 78)
    print(f"Foco de engenharia: {report['focus']}")
    print(f"Score de prontidao: {report['readiness_score']}")
    print(f"Status: {'[OK]' if report['passed'] else '[REVISAR]'}")

    print("\nGates tecnicos:")
    for gate in report["gates"]:
        status = "[OK]" if gate["passed"] else "[REVISAR]"
        print(f"- {status} {gate['name']}: {gate['value']} >= {gate['threshold']}")
        print(f"  Evidencia: {gate['evidence']}")
        print(f"  Acao: {gate['recommendation']}")

    print("\nRoteiro pratico:")
    for index, step in enumerate(report["steps"], 1):
        print(f"{index}. {step}")

    print("\nRiscos a discutir:")
    for risk in report["risks"]:
        print(f"- {risk}")

    print("\nReferencias para seguir sozinho:")
    for reference in report["references"]:
        print(f"- {reference}")


def run_check() -> int:
    """Valida estrutura minima sem imprimir o relatorio completo."""
    report = build_report()
    checks = {
        "topic_defined": bool(report["topic"]),
        "has_gates": len(report["gates"]) >= 3,
        "has_references": len(report["references"]) >= 4,
        "has_steps": len(report["steps"]) >= 3,
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        print("[FAIL] " + ", ".join(failed))
        return 1
    print("[OK] script validado")
    return 0


def main() -> int:
    """Executa o apoio da live."""
    configure_console()
    parser = argparse.ArgumentParser(description=PROFILE["topic"])
    parser.add_argument("--check", action="store_true", help="valida o script rapidamente")
    parser.add_argument("--json", action="store_true", help="imprime relatorio em JSON")
    args = parser.parse_args()

    if args.check:
        return run_check()

    report = build_report()
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
