"""CLI App — aplicação com entry point CLI, Pydantic Settings e logging JSON.

Demonstra boas práticas de configuração e CLI para ferramentas de ML.

Uso:
    python cli_app.py train --config config.env
    python cli_app.py predict --input data/input.csv
"""

import argparse
import json
import logging
import sys
from pathlib import Path
from typing import Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseSettings):
    """Configurações da aplicação via variáveis de ambiente.

    Attributes:
        model_path: Caminho para o modelo serializado.
        data_dir: Diretório de dados.
        log_level: Nível de logging.
        random_state: Seed para reprodutibilidade.
        n_estimators: Número de estimadores do modelo.
    """

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    model_path: Path = Path("models/model.pkl")
    data_dir: Path = Path("data")
    log_level: str = "INFO"
    random_state: int = 42
    n_estimators: int = 100


class JSONFormatter(logging.Formatter):
    """Formatter que emite logs em formato JSON estruturado."""

    def format(self, record: logging.LogRecord) -> str:
        """Formata o registro de log como JSON.

        Args:
            record: Registro de log.

        Returns:
            String JSON formatada.
        """
        log_data: dict[str, Any] = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "module": record.module,
            "message": record.getMessage(),
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: str = "INFO", json_format: bool = False) -> None:
    """Configura logging da aplicação.

    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR).
        json_format: Se True, usa formato JSON estruturado.
    """
    handler = logging.StreamHandler(sys.stdout)
    if json_format:
        handler.setFormatter(JSONFormatter())
    else:
        handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s"))

    logging.basicConfig(level=getattr(logging, level.upper()), handlers=[handler])


def cmd_train(args: argparse.Namespace, settings: AppSettings) -> int:
    """Executa o comando de treino.

    Args:
        args: Argumentos CLI.
        settings: Configurações da aplicação.

    Returns:
        Exit code (0 = sucesso).
    """
    logger = logging.getLogger(__name__)
    logger.info("Iniciando treinamento", extra={"model_path": str(settings.model_path)})

    from sklearn.datasets import load_iris
    from sklearn.ensemble import RandomForestClassifier
    import pickle

    X, y = load_iris(return_X_y=True)
    model = RandomForestClassifier(
        n_estimators=settings.n_estimators,
        random_state=settings.random_state,
    )
    model.fit(X, y)

    settings.model_path.parent.mkdir(parents=True, exist_ok=True)
    with open(settings.model_path, "wb") as f:
        pickle.dump(model, f)

    logger.info("Modelo salvo em: %s", settings.model_path)
    return 0


def cmd_info(args: argparse.Namespace, settings: AppSettings) -> int:
    """Exibe informações de configuração.

    Args:
        args: Argumentos CLI.
        settings: Configurações da aplicação.

    Returns:
        Exit code (0 = sucesso).
    """
    logger = logging.getLogger(__name__)
    logger.info("Configurações: %s", settings.model_dump())
    return 0


def main() -> int:
    """Entry point principal da aplicação.

    Returns:
        Exit code.
    """
    parser = argparse.ArgumentParser(
        description="MLET ML Tool — CLI para treino e inferência"
    )
    parser.add_argument("--json-logs", action="store_true", help="Habilitar logs JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("train", help="Treinar modelo")
    subparsers.add_parser("info", help="Exibir configurações")

    args = parser.parse_args()
    settings = AppSettings()
    setup_logging(settings.log_level, json_format=args.json_logs)

    commands = {"train": cmd_train, "info": cmd_info}
    cmd_fn = commands.get(args.command)
    if cmd_fn is None:
        parser.print_help()
        return 1
    return cmd_fn(args, settings)


if __name__ == "__main__":
    sys.exit(main())
