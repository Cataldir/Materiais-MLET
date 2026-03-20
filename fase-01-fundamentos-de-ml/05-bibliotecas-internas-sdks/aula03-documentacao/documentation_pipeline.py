"""Pipeline de documentacao com Template Method."""

from __future__ import annotations

import logging
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
LOGGER = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class ModuleDoc:
    """Metadados minimos de um modulo documentado."""

    name: str
    summary: str
    functions: tuple[str, ...]


@dataclass(frozen=True, slots=True)
class PackageDoc:
    """Manifesto de documentacao de um pacote interno."""

    package_name: str
    version: str
    modules: tuple[ModuleDoc, ...]


@dataclass(frozen=True, slots=True)
class DocumentationBundle:
    """Arquivos gerados pelo pipeline de documentacao."""

    files: dict[str, str]
    nav_entries: tuple[str, ...]


class DocumentationTemplate:
    """Template Method para gerar uma estrutura minima de docs."""

    def build(self, package: PackageDoc) -> DocumentationBundle:
        files = {
            "mkdocs.yml": self.render_config(package),
            "docs/index.md": self.render_index(package),
        }
        nav_entries = ["Home"]
        for module in package.modules:
            file_name = f"docs/api/{module.name}.md"
            files[file_name] = self.render_module_page(module)
            nav_entries.append(f"API/{module.name}")
        return DocumentationBundle(files=files, nav_entries=tuple(nav_entries))

    def render_config(self, package: PackageDoc) -> str:
        nav_lines = ["nav:", "  - Home: index.md"]
        for module in package.modules:
            nav_lines.append(f"  - API/{module.name}: api/{module.name}.md")
        return "\n".join(
            [
                f"site_name: {package.package_name}",
                f"site_description: Documentacao interna v{package.version}",
                *nav_lines,
            ]
        )

    def render_index(self, package: PackageDoc) -> str:
        return "\n".join(
            [
                f"# {package.package_name}",
                "",
                "Documentacao local gerada para demonstrar docstrings, navegacao e API reference.",
                "",
                "## Modulos",
                *[f"- {module.name}: {module.summary}" for module in package.modules],
            ]
        )

    def render_module_page(self, module: ModuleDoc) -> str:
        raise NotImplementedError


class MkDocsDocumentationTemplate(DocumentationTemplate):
    """Especializacao simples para paginas em Markdown."""

    def render_module_page(self, module: ModuleDoc) -> str:
        function_lines = [f"- `{function_name}`" for function_name in module.functions]
        return "\n".join(
            [
                f"# {module.name}",
                "",
                module.summary,
                "",
                "## Funcoes publicas",
                *function_lines,
                "",
                "## Exemplo de uso",
                f"`from {module.name} import {module.functions[0]}`",
            ]
        )


def build_sample_package() -> PackageDoc:
    """Constroi um manifesto pequeno de pacote interno."""

    return PackageDoc(
        package_name="ml-utils-docs",
        version="0.3.0",
        modules=(
            ModuleDoc(
                name="preprocessing",
                summary="Funcoes de limpeza e validacao para pipelines de ML.",
                functions=("clean_missing_values", "validate_feature_frame"),
            ),
            ModuleDoc(
                name="monitoring",
                summary="Helpers de metricas e alertas para servicos internos.",
                functions=("build_metrics_snapshot", "detect_quality_drop"),
            ),
        ),
    )


def build_documentation_site(package: PackageDoc | None = None) -> DocumentationBundle:
    """Executa o pipeline de documentacao para um pacote interno."""

    template = MkDocsDocumentationTemplate()
    return template.build(package or build_sample_package())


def main() -> None:
    """Imprime os arquivos gerados pelo pipeline."""

    bundle = build_documentation_site()
    LOGGER.info("Arquivos gerados: %s", sorted(bundle.files))
    LOGGER.info("Nav: %s", bundle.nav_entries)


if __name__ == "__main__":
    main()