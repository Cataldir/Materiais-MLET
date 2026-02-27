"""Hello World FastAPI — demonstração básica do framework.

Compara com hello_flask.py para mostrar diferenças de API,
validação automática e documentação interativa.

Uso:
    uvicorn hello_fastapi:app --reload
"""

import logging

from fastapi import FastAPI
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Hello FastAPI",
    description="Demonstração básica do FastAPI para inferência de modelos",
    version="1.0.0",
)


class EchoRequest(BaseModel):
    """Schema para o endpoint de echo.

    Attributes:
        message: Mensagem a ser ecoada.
        uppercase: Se True, retorna em maiúsculas.
    """

    message: str
    uppercase: bool = False


class EchoResponse(BaseModel):
    """Schema de resposta do endpoint de echo.

    Attributes:
        original: Mensagem original.
        result: Mensagem processada.
    """

    original: str
    result: str


@app.get("/")
def root() -> dict[str, str]:
    """Endpoint raiz com informações básicas.

    Returns:
        Dicionário com mensagem de boas-vindas.
    """
    return {"message": "Hello from FastAPI!", "docs": "/docs"}


@app.post("/echo", response_model=EchoResponse)
def echo(request: EchoRequest) -> EchoResponse:
    """Ecoa a mensagem recebida, opcionalmente em maiúsculas.

    Args:
        request: Dados da requisição.

    Returns:
        Resposta com mensagem original e processada.
    """
    result = request.message.upper() if request.uppercase else request.message
    logger.info("Echo: %s → %s", request.message, result)
    return EchoResponse(original=request.message, result=result)


@app.get("/health")
def health() -> dict[str, str]:
    """Health check endpoint.

    Returns:
        Status da API.
    """
    return {"status": "ok"}
