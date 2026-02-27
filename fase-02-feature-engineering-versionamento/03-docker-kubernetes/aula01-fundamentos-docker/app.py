"""Aplicação Python simples para demonstração com Docker.

API Flask mínima para demonstrar containerização com Docker.

Uso (local):
    python app.py

Uso (Docker):
    docker build -t ml-app .
    docker run -p 8000:8000 ml-app
"""

import logging
import os

from fastapi import FastAPI
import uvicorn

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

PORT = int(os.getenv("PORT", "8000"))

app = FastAPI(title="ML Docker Demo", version="1.0.0")


@app.get("/")
def root() -> dict[str, str]:
    """Endpoint raiz.

    Returns:
        Mensagem de boas-vindas.
    """
    return {"message": "ML App rodando no Docker!", "version": "1.0.0"}


@app.get("/health")
def health() -> dict[str, str]:
    """Health check.

    Returns:
        Status da aplicação.
    """
    return {"status": "ok"}


if __name__ == "__main__":
    logger.info("Iniciando servidor na porta %d", PORT)
    uvicorn.run(app, host="0.0.0.0", port=PORT)
