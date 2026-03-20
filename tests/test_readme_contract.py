"""Validate the README structure contract for canonical teaching materials."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
README_NAME = "README.md"
PHASE_GLOB = "fase-*"
REFERENCES_README = Path("referencias") / README_NAME


@dataclass(frozen=True, slots=True)
class ReadmeContract:
    """Required structure for a README scope."""

    scope: str
    required_h1_prefix: str | tuple[str, ...]
    required_sections: tuple[str, ...]
    required_one_of: tuple[tuple[str, ...], ...] = ()
    required_section_prefix: tuple[str, ...] = ()
    summary_prefix: str = ">"


@dataclass(frozen=True, slots=True)
class ReadmeCase:
    """A README path paired with the contract it must satisfy."""

    path: Path
    contract: ReadmeContract
    case_id: str


ROOT_CONTRACT = ReadmeContract(
    scope="root",
    required_h1_prefix="Materiais-MLET",
    required_sections=(
        "Papel deste repositório",
        "Arco curricular",
        "Como navegar",
        "Verdade executável versus governança canônica",
        "Visão por fase",
        "Curadoria editorial desta clone",
        "Setup rápido",
        "Comandos úteis",
        "Convenções de material executável",
        "Datasets públicos recorrentes",
        "Licença",
    ),
)

PHASE_CONTRACT = ReadmeContract(
    scope="phase",
    required_h1_prefix="Fase ",
    required_sections=(
        "Por que esta fase importa",
        "Ao concluir esta fase, você deve ser capaz de",
        "Relação com o Tech Challenge",
        "Como navegar nesta fase",
        "Disciplinas",
        "Setup",
    ),
    required_one_of=(
        ("Cobertura editorial disponível", "Como usar o material da fase"),
    ),
)

DISCIPLINE_CONTRACT = ReadmeContract(
    scope="discipline",
    required_h1_prefix=("01", "02", "03", "04", "05", "06"),
    required_sections=(
        "Por que esta disciplina importa",
        "O que você deve aprender",
        "Como usar este material",
        "Como referenciar esta disciplina no repositório",
        "Relevância para a prática executiva e acadêmica",
        "Aulas",
    ),
    required_section_prefix=(
        "Por que esta disciplina importa",
        "O que você deve aprender",
        "Como usar este material",
        "Como referenciar esta disciplina no repositório",
        "Relevância para a prática executiva e acadêmica",
        "Aulas",
    ),
)


# No GoF pattern applies — simple data-driven validation over a small contract table.
def iter_markdown_lines(markdown_text: str) -> tuple[str, ...]:
    """Return markdown lines while skipping fenced code blocks."""

    in_fence = False
    visible_lines: list[str] = []

    for raw_line in markdown_text.splitlines():
        stripped = raw_line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if not in_fence:
            visible_lines.append(raw_line)

    return tuple(visible_lines)


def extract_headings(markdown_text: str, level: int) -> tuple[str, ...]:
    """Extract headings for a given markdown level outside fenced code blocks."""

    heading_pattern = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    headings: list[str] = []

    for line in iter_markdown_lines(markdown_text):
        match = heading_pattern.match(line.strip())
        if match and len(match.group(1)) == level:
            headings.append(match.group(2))

    return tuple(headings)


def extract_link_targets(markdown_text: str) -> tuple[str, ...]:
    """Extract visible markdown link targets outside fenced code blocks."""

    link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    targets: list[str] = []

    for line in iter_markdown_lines(markdown_text):
        targets.extend(match.group(1) for match in link_pattern.finditer(line))

    return tuple(targets)


def extract_intro_line(markdown_text: str) -> str | None:
    """Return the first non-empty line after the H1 outside fenced code blocks."""

    seen_h1 = False

    for raw_line in iter_markdown_lines(markdown_text):
        stripped = raw_line.strip()
        if not stripped:
            continue
        if not seen_h1:
            if stripped.startswith("# "):
                seen_h1 = True
            continue
        return stripped

    return None


def contains_subsequence(items: tuple[str, ...], sequence: tuple[str, ...]) -> bool:
    """Return whether sequence appears in items with order preserved."""

    if not sequence:
        return True

    sequence_index = 0
    for item in items:
        if item == sequence[sequence_index]:
            sequence_index += 1
            if sequence_index == len(sequence):
                return True

    return False


def collect_phase_dirs() -> tuple[Path, ...]:
    """Return all phase directories in the canonical clone."""

    return tuple(sorted(path for path in REPO_ROOT.glob(PHASE_GLOB) if path.is_dir()))


def collect_discipline_dirs(phase_dir: Path) -> tuple[Path, ...]:
    """Return immediate discipline directories for a phase."""

    return tuple(
        sorted(
            path
            for path in phase_dir.iterdir()
            if path.is_dir() and (path / README_NAME).exists()
        )
    )


def collect_all_discipline_dirs() -> tuple[Path, ...]:
    """Return all discipline directories across the canonical clone."""

    discipline_dirs: list[Path] = []

    for phase_dir in collect_phase_dirs():
        discipline_dirs.extend(collect_discipline_dirs(phase_dir))

    return tuple(discipline_dirs)


def build_readme_cases() -> tuple[ReadmeCase, ...]:
    """Build the README validation matrix for root, phase, and discipline scopes."""

    cases = [
        ReadmeCase(
            path=REPO_ROOT / README_NAME,
            contract=ROOT_CONTRACT,
            case_id="root/README.md",
        )
    ]

    for phase_dir in collect_phase_dirs():
        phase_readme = phase_dir / README_NAME
        cases.append(
            ReadmeCase(
                path=phase_readme,
                contract=PHASE_CONTRACT,
                case_id=phase_readme.relative_to(REPO_ROOT).as_posix(),
            )
        )
        for discipline_dir in collect_discipline_dirs(phase_dir):
            discipline_readme = discipline_dir / README_NAME
            cases.append(
                ReadmeCase(
                    path=discipline_readme,
                    contract=DISCIPLINE_CONTRACT,
                    case_id=discipline_readme.relative_to(REPO_ROOT).as_posix(),
                )
            )

    return tuple(cases)


README_CASES = build_readme_cases()


def format_case_path(path: Path) -> str:
    """Return a stable display path for assertion messages."""

    try:
        return path.relative_to(REPO_ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def validate_readme_contract(path: Path, contract: ReadmeContract) -> None:
    """Assert that a README matches the required structure for its scope."""

    assert path.exists(), f"README not found: {format_case_path(path)}"

    markdown_text = path.read_text(encoding="utf-8")
    h1_headings = extract_headings(markdown_text, level=1)
    intro_line = extract_intro_line(markdown_text)
    h2_headings = extract_headings(markdown_text, level=2)
    missing_sections = [
        section for section in contract.required_sections if section not in h2_headings
    ]
    missing_section_groups = [
        section_group
        for section_group in contract.required_one_of
        if not any(section in h2_headings for section in section_group)
    ]
    required_prefix = contract.required_section_prefix
    actual_prefix = h2_headings[: len(required_prefix)]

    assert len(h1_headings) == 1, (
        f"{format_case_path(path)} must contain exactly one H1, "
        f"found {len(h1_headings)}"
    )
    assert h1_headings[0].startswith(contract.required_h1_prefix), (
        f"{format_case_path(path)} has unexpected H1 {h1_headings[0]!r} "
        f"for {contract.scope} scope"
    )
    assert intro_line is not None and intro_line.startswith(contract.summary_prefix), (
        f"{format_case_path(path)} must include a summary line starting "
        f"with {contract.summary_prefix!r} right after the H1"
    )
    assert not missing_sections, (
        f"{format_case_path(path)} is missing required sections: "
        f"{missing_sections}. Found H2 headings: {list(h2_headings)}"
    )
    assert not missing_section_groups, (
        f"{format_case_path(path)} must include at least one heading from each "
        f"alternative group: {list(missing_section_groups)}. "
        f"Found H2 headings: {list(h2_headings)}"
    )
    assert not required_prefix or contains_subsequence(h2_headings, required_prefix), (
        f"{format_case_path(path)} must preserve the ordered H2 sequence "
        f"{list(required_prefix)}. Found H2 headings: {list(h2_headings)}"
    )


@pytest.mark.parametrize(
    ("readme_path", "contract"),
    [(case.path, case.contract) for case in README_CASES],
    ids=[case.case_id for case in README_CASES],
)
def test_readme_contract(readme_path: Path, contract: ReadmeContract) -> None:
    """Each target README must satisfy the structure contract for its scope."""

    validate_readme_contract(readme_path, contract)


@pytest.mark.parametrize(
    "discipline_dir",
    collect_all_discipline_dirs(),
    ids=lambda path: path.relative_to(REPO_ROOT).as_posix(),
)
def test_discipline_referencias_contract(discipline_dir: Path) -> None:
    """Every discipline must expose and reference its local referencias index."""

    references_readme = discipline_dir / REFERENCES_README
    readme_path = discipline_dir / README_NAME
    link_targets = extract_link_targets(readme_path.read_text(encoding="utf-8"))

    assert references_readme.exists(), (
        f"Missing referencias README: {format_case_path(references_readme)}"
    )
    assert REFERENCES_README.as_posix() in link_targets, (
        f"{format_case_path(readme_path)} must link to "
        f"{REFERENCES_README.as_posix()}"
    )


def test_readme_contract_scope_inventory() -> None:
    """The canonical clone must expose the expected root and phase README scope."""

    phase_dirs = collect_phase_dirs()

    assert len(phase_dirs) == 5, (
        f"Expected 5 phase directories, found {len(phase_dirs)}: "
        f"{[path.name for path in phase_dirs]}"
    )
    assert any(case.contract.scope == "discipline" for case in README_CASES)


def test_validate_readme_contract_reports_missing_section(tmp_path: Path) -> None:
    """The validator should report which required section is missing."""

    broken_readme = tmp_path / README_NAME
    source_text = (REPO_ROOT / README_NAME).read_text(encoding="utf-8")
    broken_readme.write_text(
        source_text.replace("## Licença", "## Secao Renomeada", 1),
        encoding="utf-8",
    )

    with pytest.raises(AssertionError) as excinfo:
        validate_readme_contract(broken_readme, ROOT_CONTRACT)

    assert "Licença" in str(excinfo.value)


def test_validate_readme_contract_reports_wrong_discipline_section_order(
    tmp_path: Path,
) -> None:
    """The validator should reject discipline sections that are out of order."""

    broken_readme = tmp_path / README_NAME
    broken_readme.write_text(
        "\n".join(
            (
                "# 01 — Disciplina de Exemplo",
                "> 1h de vídeo · 1 aula",
                "",
                "## O que você deve aprender",
                "",
                "Texto.",
                "",
                "## Por que esta disciplina importa",
                "",
                "Texto.",
                "",
                "## Como usar este material",
                "",
                "Texto.",
                "",
                "## Como referenciar esta disciplina no repositório",
                "",
                "Texto.",
                "",
                "## Relevância para a prática executiva e acadêmica",
                "",
                "Texto.",
                "",
                "## Aulas",
                "",
                "- Aula 01",
            )
        ),
        encoding="utf-8",
    )

    with pytest.raises(AssertionError) as excinfo:
        validate_readme_contract(broken_readme, DISCIPLINE_CONTRACT)

    assert "must preserve the ordered H2 sequence" in str(excinfo.value)


def test_validate_readme_contract_allows_trailing_discipline_section(
    tmp_path: Path,
) -> None:
    """The validator should allow editorial H2 additions after the required core."""

    broken_readme = tmp_path / README_NAME
    broken_readme.write_text(
        "\n".join(
            (
                "# 01 — Disciplina de Exemplo",
                "> 1h de vídeo · 1 aula",
                "",
                "## Por que esta disciplina importa",
                "",
                "Texto.",
                "",
                "## O que você deve aprender",
                "",
                "Texto.",
                "",
                "## Como usar este material",
                "",
                "Texto.",
                "",
                "## Como referenciar esta disciplina no repositório",
                "",
                "Texto.",
                "",
                "## Relevância para a prática executiva e acadêmica",
                "",
                "Texto.",
                "",
                "## Aulas",
                "",
                "- Aula 01",
                "",
                "## Material complementar local",
                "",
                "Texto.",
            )
        ),
        encoding="utf-8",
    )

    validate_readme_contract(broken_readme, DISCIPLINE_CONTRACT)
