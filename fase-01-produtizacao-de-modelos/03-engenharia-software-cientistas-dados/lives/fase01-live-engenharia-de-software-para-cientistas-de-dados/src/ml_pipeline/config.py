"""Configuração do pipeline (Pydantic Settings)."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineConfig(BaseSettings):
    """Parâmetros do pipeline. Podem vir de env vars MLPIPE_*."""

    model_config = SettingsConfigDict(env_prefix="MLPIPE_")

    artifacts_dir: Path = Path("artifacts")
    target_column: str = "MedHouseVal"
    target_upper_clip: float = 5.0
    test_size: float = 0.2
    random_state: int = 42
