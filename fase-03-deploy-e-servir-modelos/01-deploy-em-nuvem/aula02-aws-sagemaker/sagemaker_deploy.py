"""AWS SageMaker Deploy — script para deploy de modelos no SageMaker.

Demonstra como empacotar e implantar modelos sklearn no SageMaker
usando o SKLearn estimator e endpoint de inferência.

Requisitos:
    pip install boto3 sagemaker

Uso:
    python sagemaker_deploy.py --model-path models/model.pkl --endpoint-name ml-endpoint
"""

import argparse
import logging
import pickle
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

REGION = "us-east-1"
INSTANCE_TYPE = "ml.t2.medium"


def package_model(model_path: Path, output_dir: Path) -> Path:
    """Empacota modelo em formato tar.gz para SageMaker.

    Args:
        model_path: Caminho para o arquivo .pkl do modelo.
        output_dir: Diretório de saída para o arquivo empacotado.

    Returns:
        Caminho para o arquivo model.tar.gz.
    """
    import io
    import tarfile

    output_dir.mkdir(parents=True, exist_ok=True)
    tar_path = output_dir / "model.tar.gz"

    with tarfile.open(tar_path, "w:gz") as tar:
        tar.add(model_path, arcname="model.pkl")

    logger.info("Modelo empacotado em: %s", tar_path)
    return tar_path


def upload_to_s3(local_path: Path, bucket: str, key: str) -> str:
    """Faz upload do modelo para S3.

    Args:
        local_path: Caminho local do arquivo.
        bucket: Nome do bucket S3.
        key: Chave S3 de destino.

    Returns:
        URI S3 do arquivo enviado.
    """
    try:
        import boto3
        s3 = boto3.client("s3", region_name=REGION)
        s3.upload_file(str(local_path), bucket, key)
        s3_uri = f"s3://{bucket}/{key}"
        logger.info("Upload concluído: %s", s3_uri)
        return s3_uri
    except ImportError:
        logger.warning("boto3 não instalado. Simulando upload para: s3://%s/%s", bucket, key)
        return f"s3://{bucket}/{key}"


def create_sagemaker_endpoint(
    model_s3_uri: str,
    endpoint_name: str,
    role_arn: str,
    instance_type: str = INSTANCE_TYPE,
) -> str:
    """Cria endpoint de inferência no SageMaker.

    Args:
        model_s3_uri: URI S3 do modelo empacotado.
        endpoint_name: Nome do endpoint a criar.
        role_arn: ARN do IAM Role com permissões SageMaker.
        instance_type: Tipo de instância para o endpoint.

    Returns:
        Nome do endpoint criado.
    """
    try:
        import boto3
        sm = boto3.client("sagemaker", region_name=REGION)

        model_name = f"{endpoint_name}-model"
        sm.create_model(
            ModelName=model_name,
            PrimaryContainer={
                "Image": f"763104351884.dkr.ecr.{REGION}.amazonaws.com/sklearn:1.2-1",
                "ModelDataUrl": model_s3_uri,
                "Environment": {"SAGEMAKER_PROGRAM": "inference.py"},
            },
            ExecutionRoleArn=role_arn,
        )

        config_name = f"{endpoint_name}-config"
        sm.create_endpoint_config(
            EndpointConfigName=config_name,
            ProductionVariants=[{
                "VariantName": "AllTraffic",
                "ModelName": model_name,
                "InitialInstanceCount": 1,
                "InstanceType": instance_type,
            }],
        )

        sm.create_endpoint(
            EndpointName=endpoint_name,
            EndpointConfigName=config_name,
        )
        logger.info("Endpoint criado: %s", endpoint_name)
    except ImportError:
        logger.warning("boto3 não disponível. Simulando criação de endpoint: %s", endpoint_name)

    return endpoint_name


def main() -> None:
    """CLI para deploy de modelo no SageMaker."""
    parser = argparse.ArgumentParser(description="Deploy de modelo no AWS SageMaker")
    parser.add_argument("--model-path", type=Path, default=Path("models/model.pkl"))
    parser.add_argument("--endpoint-name", type=str, default="ml-model-endpoint")
    parser.add_argument("--bucket", type=str, default="my-ml-bucket")
    parser.add_argument("--role-arn", type=str, default="arn:aws:iam::123456789:role/SageMakerRole")
    args = parser.parse_args()

    if not args.model_path.exists():
        logger.error("Modelo não encontrado: %s", args.model_path)
        return

    tar_path = package_model(args.model_path, Path("dist"))
    s3_uri = upload_to_s3(tar_path, args.bucket, f"models/{args.endpoint_name}/model.tar.gz")
    create_sagemaker_endpoint(s3_uri, args.endpoint_name, args.role_arn)


if __name__ == "__main__":
    main()
