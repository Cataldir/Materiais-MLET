"""Persistência dos resultados de evaluation."""

import json
from datetime import datetime, timezone
from pathlib import Path

from src.schemas import EvaluationRecord


def build_record_filename(timestamp: str) -> str:
    """Monta o nome do arquivo de output.

    Args:
        timestamp: Timestamp no formato ISO.

    Returns:
        Nome do arquivo JSON.
    """
    safe_timestamp = timestamp.replace(":", "-")
    return f"{safe_timestamp}.json"


def create_timestamp() -> str:
    """Cria um timestamp UTC em formato ISO.

    Returns:
        Timestamp ISO em UTC.
    """
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def save_evaluation_record(
    output_directory: Path,
    record: EvaluationRecord,
) -> Path:
    """Salva o registro de evaluation em JSON.

    Args:
        output_directory: Pasta de saída.
        record: Registro consolidado para persistência.

    Returns:
        Caminho do arquivo gerado.
    """
    output_directory.mkdir(parents=True, exist_ok=True)
    file_path = output_directory / build_record_filename(record.timestamp)
    with file_path.open("w", encoding="utf-8") as file:
        json.dump(record.to_dict(), file, ensure_ascii=False, indent=2)
    return file_path
