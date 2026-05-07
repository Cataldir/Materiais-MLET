"""Configuração centralizada via Pydantic Settings.

Atende ao requisito ``CLI com Pydantic Settings``. Uma única razão de
mudança: parâmetros operacionais do pipeline.
"""

from __future__ import annotations

from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class PipelineConfig(BaseSettings):
    """Parâmetros do pipeline de treino e avaliação.

    Variáveis de ambiente com prefixo ``MLPIPE_`` sobrescrevem os defaults.
    Flags da CLI sobrescrevem ambos.
    """

    model_config = SettingsConfigDict(env_prefix="MLPIPE_", env_file=".env")

    artifacts_dir: Path = Field(default=Path("artifacts"))
    target_column: str = Field(default="MedHouseVal")
    target_upper_clip: float = Field(default=5.0, gt=0)
    test_size: float = Field(default=0.2, gt=0, lt=1)
    random_state: int = Field(default=42, ge=0)
