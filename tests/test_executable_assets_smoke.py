"""Lightweight smoke coverage for repository-wide executable assets."""

from __future__ import annotations

from pathlib import Path

import pytest

from tools.repo_tasks import (
    iter_notebook_assets,
    iter_python_assets,
    validate_notebook_asset,
    validate_python_asset,
)

PYTHON_ASSETS = iter_python_assets()
NOTEBOOK_ASSETS = iter_notebook_assets()


def asset_id(path: Path) -> str:
    """Return stable pytest ids relative to the repository root."""

    return path.as_posix()


@pytest.mark.parametrize("python_path", PYTHON_ASSETS, ids=asset_id)
def test_python_assets_compile(python_path: Path) -> None:
    """Every tracked Python asset should parse as valid Python."""

    validate_python_asset(python_path)


@pytest.mark.parametrize("notebook_path", NOTEBOOK_ASSETS, ids=asset_id)
def test_notebook_assets_are_structurally_valid(notebook_path: Path) -> None:
    """Every tracked notebook should load as JSON and contain valid code cells."""

    validate_notebook_asset(notebook_path)