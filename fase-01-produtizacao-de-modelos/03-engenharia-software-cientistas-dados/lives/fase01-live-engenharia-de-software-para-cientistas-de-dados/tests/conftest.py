"""Fixtures comuns à suíte."""

from __future__ import annotations

import pandas as pd
import pytest

from ml_pipeline.data import load_california_housing


@pytest.fixture(scope="session")
def raw_dataset() -> pd.DataFrame:
    return load_california_housing()


@pytest.fixture(scope="session")
def small_raw_dataset(raw_dataset: pd.DataFrame) -> pd.DataFrame:
    """Subamostra fixa para testes que não precisam do dataset inteiro."""
    return raw_dataset.sample(n=2000, random_state=0).reset_index(drop=True)
