"""Projeto integrador local da disciplina de inferencia causal."""

from __future__ import annotations

import logging
from dataclasses import dataclass

LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CausalProjectRow:
    """Linha consolidada do projeto causal."""

    component: str
    key_signal: str
    decision: str


@dataclass(frozen=True, slots=True)
class CausalProjectSummary:
    """Resumo executivo do projeto final."""

    rows: tuple[CausalProjectRow, ...]
    priority_queue: tuple[str, ...]
    governance_note: str


def run_causal_project() -> CausalProjectSummary:
    """Consolida o workflow causal da disciplina em um unico resumo."""

    rows = (
        CausalProjectRow(
            component="dag_scm",
            key_signal="efeito medio estimado da campanha acima de 40 unidades de receita",
            decision="manter o tratamento como alavanca valida para experimento",
        ),
        CausalProjectRow(
            component="uplift_modeling",
            key_signal="segmento alto_potencial lidera o ranking incremental",
            decision="priorizar comunicacao para alto_potencial antes dos demais segmentos",
        ),
        CausalProjectRow(
            component="prescriptive_monitoring",
            key_signal="segmento reativacao exige analise de risco antes de ampliar incentivo",
            decision="abrir revisao conjunta entre operacao e governanca",
        ),
    )
    return CausalProjectSummary(
        rows=rows,
        priority_queue=("alto_potencial", "reativacao", "baixo_risco"),
        governance_note="documentar efeito estimado, segmento acionado e criterio de escalonamento em cada ciclo",
    )


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    summary = run_causal_project()
    for row in summary.rows:
        LOGGER.info("%s | %s | %s", row.component, row.key_signal, row.decision)
    LOGGER.info("priority_queue=%s", list(summary.priority_queue))
    LOGGER.info(summary.governance_note)


if __name__ == "__main__":
    main()