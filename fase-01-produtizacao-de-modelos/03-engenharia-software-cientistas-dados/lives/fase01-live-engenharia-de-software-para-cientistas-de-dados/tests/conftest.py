"""Fixtures compartilhadas."""

import pytest

from ml_pipeline.data import load_data


@pytest.fixture(scope="session")
def raw_df():
    return load_data()
