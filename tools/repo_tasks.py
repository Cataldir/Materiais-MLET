"""Cross-platform task runner and reusable repository validation helpers."""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKIP_DIR_NAMES = {
    ".git",
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp_test_mlflow_monitoring",
    ".venv",
    "__pycache__",
    "htmlcov",
}
CLEAN_DIR_NAMES = {
    ".ipynb_checkpoints",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".tmp_test_mlflow_monitoring",
    "__pycache__",
    "build",
    "dist",
    "htmlcov",
}
CLEAN_FILE_NAMES = {
    ".coverage",
    "notebooks_check.log",
    "validate_bootstrap.log",
}
CLEAN_FILE_GLOBS = ("*.pyc", ".coverage.*")
MAKE_HELP_PATTERN = re.compile(r"^([A-Za-z0-9_.-]+):.*?##\s+(.*)$")


def iter_repo_files(*suffixes: str) -> tuple[Path, ...]:
    """Return repository files while pruning generated folders."""

    files: list[Path] = []
    normalized_suffixes = {suffix.lower() for suffix in suffixes}

    for root, dirnames, filenames in os.walk(REPO_ROOT):
        dirnames[:] = [
            dirname for dirname in sorted(dirnames) if dirname not in SKIP_DIR_NAMES
        ]
        current_root = Path(root)

        for filename in sorted(filenames):
            candidate = current_root / filename
            if candidate.suffix.lower() in normalized_suffixes:
                files.append(candidate.relative_to(REPO_ROOT))

    return tuple(files)


def iter_python_assets() -> tuple[Path, ...]:
    """Return Python assets for lightweight syntax validation."""

    return iter_repo_files(".py")


def iter_notebook_assets() -> tuple[Path, ...]:
    """Return notebook assets for lightweight structural validation."""

    return iter_repo_files(".ipynb")


def validate_python_asset(path: Path) -> None:
    """Assert that a Python file parses successfully."""

    source = (REPO_ROOT / path).read_text(encoding="utf-8")
    compile(source, str(path), "exec")


def validate_notebook_asset(path: Path) -> int:
    """Assert that a notebook loads and its code cells parse successfully."""

    notebook = json.loads((REPO_ROOT / path).read_text(encoding="utf-8"))
    cells = notebook.get("cells")

    if not isinstance(cells, list):
        raise AssertionError(f"{path.as_posix()} is missing a valid cells array")

    code_cell_count = 0
    for index, cell in enumerate(cells, start=1):
        if not isinstance(cell, dict):
            raise AssertionError(f"{path.as_posix()} has a non-object cell at index {index}")
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", [])
        if isinstance(source, list):
            source_text = "".join(source)
        elif isinstance(source, str):
            source_text = source
        else:
            raise AssertionError(
                f"{path.as_posix()} has an invalid source payload in code cell {index}"
            )
        compile(source_text, f"{path.as_posix()}::cell-{index}", "exec")
        code_cell_count += 1

    return code_cell_count


def run_pre_commit(files: list[str] | None = None) -> int:
    """Run the repository pre-commit suite with the current Python interpreter."""

    command = [sys.executable, "-m", "pre_commit", "run"]
    if files:
        command.extend(["--files", *files])
    else:
        command.append("--all-files")

    completed = subprocess.run(command, cwd=REPO_ROOT, check=False)
    return completed.returncode


def command_notebooks_check() -> int:
    """Run the lightweight notebook smoke validation and print a summary."""

    notebook_assets = iter_notebook_assets()
    total_code_cells = 0

    for notebook_path in notebook_assets:
        try:
            total_code_cells += validate_notebook_asset(notebook_path)
        except Exception as error:  # pragma: no cover - surfaced to the CLI user
            print(
                f"notebook check failed for {notebook_path.as_posix()}: {error}",
                file=sys.stderr,
            )
            return 1

    print(
        "notebooks-check passed: "
        f"{len(notebook_assets)} notebooks, {total_code_cells} code cells"
    )
    return 0


def command_clean() -> int:
    """Remove generated local artifacts in a cross-platform way."""

    removed_paths: list[str] = []

    for root, dirnames, filenames in os.walk(REPO_ROOT):
        current_root = Path(root)

        for dirname in list(dirnames):
            if dirname in CLEAN_DIR_NAMES or dirname.endswith(".egg-info"):
                target = current_root / dirname
                shutil.rmtree(target, ignore_errors=True)
                removed_paths.append(target.relative_to(REPO_ROOT).as_posix())
                dirnames.remove(dirname)

        for filename in filenames:
            target = current_root / filename
            if filename in CLEAN_FILE_NAMES or any(
                target.match(pattern) for pattern in CLEAN_FILE_GLOBS
            ):
                target.unlink(missing_ok=True)
                removed_paths.append(target.relative_to(REPO_ROOT).as_posix())

    if removed_paths:
        print(f"clean removed {len(removed_paths)} paths")
    else:
        print("clean found no generated paths to remove")
    return 0


def command_make_help() -> int:
    """Render Makefile help text without Unix-only shell tools."""

    makefile_path = REPO_ROOT / "Makefile"
    targets: list[tuple[str, str]] = []

    for line in makefile_path.read_text(encoding="utf-8").splitlines():
        match = MAKE_HELP_PATTERN.match(line)
        if match:
            targets.append((match.group(1), match.group(2)))

    for target, description in sorted(targets):
        print(f"{target:<22} {description}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI parser for repository utility commands."""

    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser(
        "validate", help="run the repository pre-commit validation suite"
    )
    validate_parser.add_argument(
        "files",
        nargs="*",
        help="optional file list; when omitted the full repository is validated",
    )

    subparsers.add_parser(
        "notebooks-check",
        help="run lightweight structural checks for all tracked notebooks",
    )
    subparsers.add_parser(
        "clean", help="remove generated caches and local validation artifacts"
    )
    subparsers.add_parser(
        "make-help", help="render Makefile help output without Unix-only tools"
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Dispatch repository utility commands."""

    args = build_parser().parse_args(argv)

    if args.command == "validate":
        return run_pre_commit(args.files)
    if args.command == "notebooks-check":
        return command_notebooks_check()
    if args.command == "clean":
        return command_clean()
    if args.command == "make-help":
        return command_make_help()
    raise RuntimeError(f"Unsupported command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())