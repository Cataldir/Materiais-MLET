"""Update discipline READMEs from ementa governance files.

Reads each ementa from the mlet governance repo and rewrites the
corresponding Materiais-MLET discipline README with:
- Proper title and lesson count
- Abstract (non-reproducing summary of key ideas)
- Lesson plan table (titles + key topics)
- Key references
- Tools/libraries used
"""

import os
import re
from pathlib import Path

MLET = Path(r"C:\Users\ricar\Github\mlet")
MAT = Path(r"C:\Users\ricar\Github\Materiais-MLET")

MAPPING = {
    # (phase_folder, ementa_filename): materiais_discipline_folder
    # Fase 02
    ("fase-02-containers-e-ambientes-reprodutiveis", "Clean Code para Engenharia de ML.md"): "fase-02-containers-e-ambientes-reprodutiveis/01-clean-code-ml",
    ("fase-02-containers-e-ambientes-reprodutiveis", "Gerenciamento de Depend\u00eancias.md"): "fase-02-containers-e-ambientes-reprodutiveis/02-gerenciamento-dependencias",
    ("fase-02-containers-e-ambientes-reprodutiveis", "Docker e Kubernetes.md"): "fase-02-containers-e-ambientes-reprodutiveis/03-docker-kubernetes",
    ("fase-02-containers-e-ambientes-reprodutiveis", "Controle de Vers\u00e3o de Dados e Modelos.md"): "fase-02-containers-e-ambientes-reprodutiveis/04-dvc-mlflow",
    # Fase 03
    ("fase-03-cloud-e-mlops", "Deploy em nuvem.md"): "fase-03-cloud-e-mlops/01-deploy-em-nuvem",
    ("fase-03-cloud-e-mlops", "Integra\u00e7\u00e3o com CICD.md"): "fase-03-cloud-e-mlops/02-integracao-cicd",
    ("fase-03-cloud-e-mlops", "Pipeline ML.md"): "fase-03-cloud-e-mlops/03-pipeline-treino-deploy-automatico",
    ("fase-03-cloud-e-mlops", "Monitoracao Performance.md"): "fase-03-cloud-e-mlops/04-monitoracao-performance",
    ("fase-03-cloud-e-mlops", "Servicos de Monitoracao.md"): "fase-03-cloud-e-mlops/05-servicos-de-monitoracao",
    ("fase-03-cloud-e-mlops", "Latencia e Performance.md"): "fase-03-cloud-e-mlops/06-latencia-performance",
    # Fase 04
    ("fase-04-monitoramento-e-governanca", "Data Drift.md"): "fase-04-monitoramento-e-governanca/01-data-drift",
    ("fase-04-monitoramento-e-governanca", "Monitoramento de Modelos.md"): "fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos",
    ("fase-04-monitoramento-e-governanca", "Monitoramento de Pipelines.md"): "fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra",
    ("fase-04-monitoramento-e-governanca", "Valida\u00e7\u00e3o de Dados em ML.md"): "fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade",
    ("fase-04-monitoramento-e-governanca", "Governan\u00e7a e Compliance.md"): "fase-04-monitoramento-e-governanca/05-governanca-compliance",
    ("fase-04-monitoramento-e-governanca", "Infer\u00eancia Causal.md"): "fase-04-monitoramento-e-governanca/06-inferencia-causal",
    # Fase 05
    ("fase-05-deploy-avancado-de-ia-generativa", "Deploy de LLMs.md"): "fase-05-deploy-avancado-de-ia-generativa/01-deploy-modelos-ia-generativa",
    ("fase-05-deploy-avancado-de-ia-generativa", "Deploy de Agentes.md"): "fase-05-deploy-avancado-de-ia-generativa/02-deploy-agentes-llms",
    ("fase-05-deploy-avancado-de-ia-generativa", "Aplicacoes Avancadas.md"): "fase-05-deploy-avancado-de-ia-generativa/03-aplicacoes-avancadas-escalabilidade",
    ("fase-05-deploy-avancado-de-ia-generativa", "Avalia\u00e7\u00e3o e Observabilidade.md"): "fase-05-deploy-avancado-de-ia-generativa/04-avaliacao-observabilidade-llmops",
    ("fase-05-deploy-avancado-de-ia-generativa", "Seguran\u00e7a Guardrails e Conformidade.md"): "fase-05-deploy-avancado-de-ia-generativa/05-seguranca-guardrails-conformidade",
}


def parse_ementa(path: Path) -> dict:
    """Parse an ementa markdown file into structured data."""
    content = path.read_text(encoding="utf-8")

    # Title
    title_match = re.search(r"^#\s+(.+)$", content, re.MULTILINE)
    title = title_match.group(1).strip() if title_match else path.stem

    # Try table format first (| col1 | col2 | ...)
    table_rows = []
    header_cols = []
    in_table = False
    for line in content.split("\n"):
        stripped = line.strip()
        if stripped.startswith("|") and "---" not in stripped:
            cols = [c.strip() for c in stripped.split("|")[1:-1]]
            if not in_table:
                header_cols = [c.lower() for c in cols]
                in_table = True
            else:
                table_rows.append(cols)
        elif in_table and not stripped.startswith("|"):
            break

    lessons = []
    if table_rows:
        # Determine column indices from header
        title_idx = 0
        topic_idx = None
        ref_idx = None
        for i, h in enumerate(header_cols):
            if "tema" in h and "central" in h:
                topic_idx = i
            elif "tema" in h and topic_idx is None:
                topic_idx = i
            elif "refer" in h:
                ref_idx = i
        # Fallback: topic is col after title (skip date cols)
        if topic_idx is None:
            for i, h in enumerate(header_cols):
                if i > 0 and not re.match(r"data|entrega", h):
                    topic_idx = i
                    break
            if topic_idx is None:
                topic_idx = 1
        if ref_idx is None:
            ref_idx = len(header_cols) - 1

        for row in table_rows:
            if len(row) >= 2:
                lesson_title = row[title_idx] if title_idx < len(row) else f"Aula {len(lessons)+1}"
                topic = row[topic_idx] if topic_idx < len(row) else ""
                ref = row[ref_idx] if ref_idx < len(row) else ""
                lessons.append({
                    "title": lesson_title,
                    "topic": topic[:120],
                    "reference": ref,
                })
    else:
        # Header format: ### Aula N: **Title**
        for match in re.finditer(
            r"###\s+Aula\s+\d+[:\s]*\*{0,2}(.+?)\*{0,2}\s*$", content, re.MULTILINE
        ):
            lesson_title = match.group(1).strip().strip("*")
            # Get the first "O quê:" line after this header
            pos = match.end()
            topic_match = re.search(
                r"\*\*O qu[eê]:\*\*\s*(.+?)(?:\n\n|\n-)", content[pos:pos+500], re.DOTALL
            )
            topic = ""
            if topic_match:
                topic = topic_match.group(1).strip()[:120]
            lessons.append({
                "title": lesson_title,
                "topic": topic,
                "reference": "",
            })

    # Extract unique references
    refs = set()
    for lesson in lessons:
        ref = lesson["reference"]
        if ref:
            # Extract author and year
            match = re.search(r"([A-Z][a-zà-ü]+(?:\s+(?:et\s+al\.|[A-Z]))?[^(]*)\((\d{4})\)", ref)
            if match:
                refs.add(f"{match.group(1).strip()} ({match.group(2)})")
            else:
                # Try to get first meaningful part
                short = ref.split(".")[0].strip()[:80]
                if short:
                    refs.add(short)

    # Extract tools from content
    tools_section = set()
    tool_patterns = [
        r"(?:Python|Docker|Kubernetes|Helm|Prometheus|Grafana|MLflow|DVC|"
        r"FastAPI|Flask|PyTorch|TensorFlow|scikit-learn|Airflow|"
        r"LangChain|FAISS|Chroma|vLLM|Ray|OpenTelemetry|"
        r"Great Expectations|Pandera|Pydantic|Evidently|"
        r"GitHub Actions|AWS|Azure|GCP|Kubeflow|"
        r"NVIDIA|ONNX|TensorRT|BentoML|Langfuse|"
        r"Poetry|UV|Git|Jenkins|ELK|Datadog)"
    ]
    for pattern in tool_patterns:
        for m in re.finditer(pattern, content):
            tools_section.add(m.group(0))

    return {
        "title": title,
        "lessons": lessons,
        "num_lessons": len(lessons),
        "references": sorted(refs)[:5],
        "tools": sorted(tools_section),
    }


def generate_readme(ementa_data: dict, discipline_slug: str) -> str:
    """Generate a discipline README from parsed ementa data."""
    d = ementa_data
    num = discipline_slug.split("/")[-1].split("-")[0]

    lines = []
    lines.append(f"# {num} — {d['title']}\n")
    lines.append(f"> {d['num_lessons']} aulas · ~{d['num_lessons'] * 45}min de video\n")
    lines.append("")
    lines.append("## Resumo da Disciplina\n")

    # Generate abstract from lesson topics
    topics_summary = "; ".join(
        lesson["title"].split("–")[-1].strip() if "–" in lesson["title"]
        else lesson["title"].split("—")[-1].strip() if "—" in lesson["title"]
        else lesson["title"]
        for lesson in d["lessons"][:4]
    )
    lines.append(
        f"Esta disciplina cobre {d['num_lessons']} temas progressivos: "
        f"desde fundamentos até aplicação em produção. "
        f"Os primeiros temas abordam: {topics_summary}.\n"
    )
    lines.append("")

    # Lesson plan table
    lines.append("## Plano de Aulas\n")
    lines.append("| # | Tema | Tópico Central |")
    lines.append("|---|------|----------------|")
    for i, lesson in enumerate(d["lessons"], 1):
        title = lesson["title"]
        topic = lesson["topic"][:80] + "..." if len(lesson["topic"]) > 80 else lesson["topic"]
        lines.append(f"| {i:02d} | {title} | {topic} |")
    lines.append("")

    # Tools
    if d["tools"]:
        lines.append("## Ferramentas e Bibliotecas\n")
        lines.append(", ".join(d["tools"]))
        lines.append("")

    # References
    if d["references"]:
        lines.append("## Referências Principais\n")
        for ref in d["references"][:5]:
            lines.append(f"- {ref}")
        lines.append("")

    # Usage note
    lines.append("## Como Usar\n")
    lines.append("1. Siga as aulas na ordem numérica.")
    lines.append("2. Execute os scripts/notebooks de cada aula localmente.")
    lines.append("3. Consulte `referencias/README.md` para leituras complementares.")
    lines.append("")

    return "\n".join(lines)


def main():
    updated = 0
    for (fase, ementa_file), mat_rel in MAPPING.items():
        ementa_path = MLET / "fases" / fase / "governanca-da-fase" / "ementas" / ementa_file
        target_readme = MAT / mat_rel / "README.md"

        if not ementa_path.exists():
            print(f"SKIP (no ementa): {ementa_file}")
            continue
        if not target_readme.exists():
            print(f"SKIP (no target): {mat_rel}")
            continue

        ementa_data = parse_ementa(ementa_path)
        new_content = generate_readme(ementa_data, mat_rel)
        target_readme.write_text(new_content, encoding="utf-8")
        updated += 1
        print(f"OK: {mat_rel} ({ementa_data['num_lessons']} aulas)")

    print(f"\nUpdated {updated} discipline READMEs.")


if __name__ == "__main__":
    main()
