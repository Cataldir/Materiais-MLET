# MLflow para Tracking e Model Registry

## MLflow no Contexto de Observabilidade

MLflow não é uma ferramenta de monitoramento em tempo real — é uma ferramenta de **linhagem e rastreabilidade**. Enquanto Prometheus responde "como o modelo está agora?", MLflow responde "qual modelo é esse, como foi treinado, e quais foram seus resultados?".

## Componentes do MLflow

### 1. Tracking

Registra parâmetros, métricas e artefatos de cada execução de treino:

```python
import mlflow

with mlflow.start_run(run_name="iris-rf-v3"):
    mlflow.log_param("n_estimators", 100)
    mlflow.log_param("max_depth", 5)
    mlflow.log_param("dataset_version", "2026-04-01")

    # Métricas de treino
    mlflow.log_metric("train_accuracy", 0.95)
    mlflow.log_metric("val_accuracy", 0.93)
    mlflow.log_metric("train_f1", 0.94)

    # Artefatos
    mlflow.sklearn.log_model(model, "model")
    mlflow.log_artifact("feature_importance.png")
```

### 2. Model Registry

Ciclo de vida de modelos com estágios:

```
None → Staging → Production → Archived
```

```python
# Registrar modelo
result = mlflow.register_model(
    model_uri=f"runs:/{run_id}/model",
    name="iris-classifier"
)

# Transicionar para produção
client = mlflow.tracking.MlflowClient()
client.transition_model_version_stage(
    name="iris-classifier",
    version=result.version,
    stage="Production"
)
```

### 3. Integração com Prometheus

A ponte entre MLflow e Prometheus acontece no código da aplicação:

```python
# Ao carregar modelo do registry, registrar métrica
model_info = client.get_model_version_by_alias("iris-classifier", "champion")
MODEL_VERSION_GAUGE.labels(
    model_name="iris-classifier"
).set(int(model_info.version))

# Ao treinar, exportar métricas de treino para Prometheus
TRAINING_ACCURACY.set(val_accuracy)
TRAINING_LOSS.set(val_loss)
```

Isso permite que o Grafana mostre tanto métricas operacionais (do Prometheus) quanto contexto do modelo (via métricas exportadas do MLflow) em um único dashboard.

## MLflow Tracking Server

Para ambiente multi-usuário, o MLflow roda como servidor centralizado:

```bash
mlflow server \
    --backend-store-uri postgresql://user:pass@db:5432/mlflow \
    --default-artifact-root s3://mlflow-artifacts/ \
    --host 0.0.0.0 \
    --port 5000
```

Na nossa aula, usamos SQLite e armazenamento local via Docker Compose para simplicidade.

## Boas Práticas

1. **Sempre versione os dados** junto com o modelo (log do hash ou versão do dataset)
2. **Use tags** para organizar experimentos (`team`, `project`, `environment`)
3. **Registre métricas por epoch** para diagnóstico de treino
4. **Automatize a promoção** de modelos com base em métricas do Prometheus
5. **Conecte alertas de drift** ao retreino automático via MLflow
