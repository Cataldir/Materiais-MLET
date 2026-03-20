"""Workflow de formatacao com Command sobre snippets Python."""

from __future__ import annotations

import logging
import re
from collections.abc import Callable
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class CodeSample:
    """Snippet antes e depois da formatacao."""

    name: str
    source: str


@dataclass(frozen=True, slots=True)
class FormatCommand:
    """Comando de formatacao sobre texto."""

    name: str
    operation: Callable[[str], str]

    def run(self, source: str) -> str:
        return self.operation(source)


def normalize_indentation(source: str) -> str:
    return source.replace("\t", "    ")


def strip_trailing_whitespace(source: str) -> str:
    return "\n".join(line.rstrip() for line in source.splitlines())


def normalize_blank_lines(source: str) -> str:
    return re.sub(r"\n{3,}", "\n\n", source)


def camel_to_snake(value: str) -> str:
    first_pass = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", value)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", first_pass).lower()


def normalize_identifier_names(source: str) -> str:
    pattern = re.compile(r"\b[A-Za-z][A-Za-z0-9]*\b")

    def repl(match: re.Match[str]) -> str:
        name = match.group(0)
        if name in {"def", "return"}:
            return name
        return camel_to_snake(name) if any(char.isupper() for char in name) else name

    return pattern.sub(repl, source)


def build_formatting_commands() -> tuple[FormatCommand, ...]:
    """Constroi a fila de comandos de formatacao da aula."""

    return (
        FormatCommand("indentation", normalize_indentation),
        FormatCommand("trailing_whitespace", strip_trailing_whitespace),
        FormatCommand("blank_lines", normalize_blank_lines),
        FormatCommand("naming", normalize_identifier_names),
    )


def run_formatting_workflow(samples: tuple[CodeSample, ...] | None = None) -> dict[str, str]:
    """Aplica o workflow de formatacao aos snippets fornecidos."""

    effective_samples = samples or (
        CodeSample(
            name="before.py",
            source=(
                "ModelScore = 0.91  \n"
                "\tdef buildModel():\n"
                "\t\treturn ModelScore\n\n\n"
            ),
        ),
    )
    commands = build_formatting_commands()
    formatted: dict[str, str] = {}

    for sample in effective_samples:
        source = sample.source
        for command in commands:
            source = command.run(source)
        formatted[sample.name] = source + "\n"
    return formatted


def main() -> None:
    """Executa o workflow e imprime o snippet formatado."""

    result = run_formatting_workflow()
    for name, source in result.items():
        LOGGER.info("Arquivo: %s", name)
        print(source)


if __name__ == "__main__":
    main()