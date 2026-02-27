"""AWS Lambda Handler — função Lambda para inferência serverless.

Demonstra como criar uma função Lambda para inferência de modelo ML
com carregamento do modelo do S3.

Deploy:
    zip -r lambda.zip lambda_handler.py
    aws lambda update-function-code --function-name ml-inference --zip-file fileb://lambda.zip
"""

import json
import logging
import os
import pickle
import tempfile
from typing import Any

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

MODEL_BUCKET = os.environ.get("MODEL_BUCKET", "my-ml-bucket")
MODEL_KEY = os.environ.get("MODEL_KEY", "models/model.pkl")

_model: Any = None


def load_model() -> Any:
    """Carrega modelo do S3 (com cache em memória entre invocações).

    Returns:
        Modelo sklearn carregado.
    """
    global _model
    if _model is not None:
        return _model

    try:
        import boto3
        s3 = boto3.client("s3")
        with tempfile.NamedTemporaryFile(suffix=".pkl") as tmp:
            s3.download_file(MODEL_BUCKET, MODEL_KEY, tmp.name)
            with open(tmp.name, "rb") as f:
                _model = pickle.load(f)  # noqa: S301
        logger.info("Modelo carregado do S3: s3://%s/%s", MODEL_BUCKET, MODEL_KEY)
    except ImportError:
        logger.warning("boto3 não disponível em ambiente local")
        _model = None
    return _model


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    """Handler principal da função Lambda.

    Args:
        event: Evento Lambda com payload da requisição.
        context: Contexto de execução Lambda.

    Returns:
        Resposta HTTP formatada para API Gateway.
    """
    logger.info("Evento recebido: %s", json.dumps(event))

    try:
        body = json.loads(event.get("body", "{}"))
        features = body.get("features", [])

        if not features:
            return {
                "statusCode": 400,
                "body": json.dumps({"error": "Campo 'features' obrigatório"}),
            }

        model = load_model()
        if model is None:
            return {
                "statusCode": 503,
                "body": json.dumps({"error": "Modelo não disponível"}),
            }

        import numpy as np
        X = np.array(features).reshape(1, -1)
        prediction = float(model.predict(X)[0])
        probability = None
        if hasattr(model, "predict_proba"):
            probability = float(model.predict_proba(X).max())

        return {
            "statusCode": 200,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps({
                "prediction": prediction,
                "probability": probability,
            }),
        }

    except Exception as exc:
        logger.error("Erro na inferência: %s", exc)
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(exc)}),
        }
