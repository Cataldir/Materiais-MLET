"""Checklist de reprodutibilidade para projetos de ML.

Verifica e documenta elementos essenciais para garantir que
experimentos possam ser reproduzidos por outros pesquisadores.

Uso:
    python reproducibility_checklist.py
"""

import hashlib
import logging
import platform
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


@dataclass
class ReproducibilityReport:
    """Relatório de reprodutibilidade do ambiente.

    Attributes:
        python_version: Versão do Python.
        platform_info: Informações da plataforma.
        installed_packages: Pacotes instalados com versões.
        seed_set: Se seeds foram configurados.
        data_hashes: Hashes dos arquivos de dados.
        issues: Problemas encontrados.
    """

    python_version: str = ""
    platform_info: str = ""
    installed_packages: dict[str, str] = field(default_factory=dict)
    seed_set: bool = False
    data_hashes: dict[str, str] = field(default_factory=dict)
    issues: list[str] = field(default_factory=list)

    def is_reproducible(self) -> bool:
        """Verifica se o ambiente está configurado para reprodutibilidade.

        Returns:
            True se não há issues críticos, False caso contrário.
        """
        return len(self.issues) == 0


def get_python_environment() -> tuple[str, str]:
    """Coleta informações do ambiente Python.

    Returns:
        Tupla (versão Python, informações da plataforma).
    """
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    platform_info = f"{platform.system()} {platform.release()} ({platform.machine()})"
    return python_version, platform_info


def get_installed_packages() -> dict[str, str]:
    """Lista pacotes instalados com suas versões.

    Returns:
        Dicionário {pacote: versão}.
    """
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "list", "--format=json"],
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )
        import json

        packages = json.loads(result.stdout)
        return {pkg["name"]: pkg["version"] for pkg in packages}
    except Exception as exc:
        logger.warning("Não foi possível listar pacotes: %s", exc)
        return {}


def hash_file(file_path: Path) -> str:
    """Calcula hash SHA-256 de um arquivo.

    Args:
        file_path: Caminho para o arquivo.

    Returns:
        Hash SHA-256 hexadecimal.
    """
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def check_seeds_in_code(code_dir: Path) -> bool:
    """Verifica se seeds aleatórias estão definidas nos scripts Python.

    Args:
        code_dir: Diretório com scripts Python.

    Returns:
        True se seeds foram encontradas, False caso contrário.
    """
    seed_patterns = [
        "random_state=",
        "np.random.seed(",
        "torch.manual_seed(",
        "RANDOM_STATE",
    ]
    for py_file in code_dir.glob("*.py"):
        content = py_file.read_text()
        if any(pattern in content for pattern in seed_patterns):
            return True
    return False


def generate_report(project_dir: Path = Path(".")) -> ReproducibilityReport:
    """Gera relatório completo de reprodutibilidade.

    Args:
        project_dir: Diretório raiz do projeto.

    Returns:
        Relatório de reprodutibilidade.
    """
    report = ReproducibilityReport()
    report.python_version, report.platform_info = get_python_environment()
    report.installed_packages = get_installed_packages()

    pyproject = project_dir / "pyproject.toml"
    requirements = project_dir / "requirements.txt"
    if not pyproject.exists() and not requirements.exists():
        report.issues.append(
            "Nenhum arquivo de dependências encontrado (pyproject.toml ou requirements.txt)"
        )

    report.seed_set = check_seeds_in_code(project_dir)
    if not report.seed_set:
        report.issues.append("Seeds aleatórias não encontradas nos scripts Python")

    data_dir = project_dir / "data"
    if data_dir.exists():
        for data_file in data_dir.glob("*.csv"):
            report.data_hashes[data_file.name] = hash_file(data_file)
    else:
        report.issues.append("Diretório 'data/' não encontrado")

    logger.info("=== Relatório de Reprodutibilidade ===")
    logger.info(
        "Python: %s | Platform: %s", report.python_version, report.platform_info
    )
    logger.info("Pacotes instalados: %d", len(report.installed_packages))
    logger.info("Seeds configuradas: %s", "✓" if report.seed_set else "✗")
    logger.info("Hashes de dados: %d arquivos", len(report.data_hashes))

    if report.issues:
        for issue in report.issues:
            logger.warning("Issue: %s", issue)
    else:
        logger.info("✓ Projeto está configurado para reprodutibilidade")

    return report


if __name__ == "__main__":
    generate_report()
