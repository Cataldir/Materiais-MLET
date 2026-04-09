# Instrumentação de Pipelines Observáveis

## Princípio: Instrumentar Primeiro, Otimizar Depois

Antes de se preocupar com performance ou escalabilidade, garanta que cada etapa do pipeline emite métricas. Um pipeline sem métricas é como dirigir à noite sem faróis — você não sabe que está saindo da pista até bater.

## Pipeline de Treino Observável

### Métricas que Devem Ser Emitidas

```
┌─────────────────────────────────────────────────────────┐
│                 PIPELINE DE TREINO                       │
├────────────┬────────────┬────────────┬──────────────────┤
│ Ingestão   │ Validação  │ Treino     │ Avaliação        │
├────────────┼────────────┼────────────┼──────────────────┤
│ rows_read  │ null_count │ epoch_loss │ val_accuracy     │
│ file_size  │ schema_ok  │ epoch_acc  │ val_f1           │
│ load_time  │ drift_score│ lr_current │ inference_time   │
│ feature_ct │ outlier_ct │ gpu_util   │ model_size_bytes │
└────────────┴────────────┴────────────┴──────────────────┘
```

### Exemplo: Métricas por Epoch

```python
from prometheus_client import Gauge, Histogram

EPOCH_LOSS = Gauge('training_epoch_loss', 'Loss na epoch atual', ['experiment'])
EPOCH_ACC = Gauge('training_epoch_accuracy', 'Accuracy na epoch atual', ['experiment'])
EPOCH_DURATION = Histogram(
    'training_epoch_duration_seconds',
    'Duração de cada epoch',
    buckets=[10, 30, 60, 120, 300]
)

for epoch in range(num_epochs):
    with EPOCH_DURATION.time():
        loss, acc = train_one_epoch(model, data)

    EPOCH_LOSS.labels(experiment="iris-rf").set(loss)
    EPOCH_ACC.labels(experiment="iris-rf").set(acc)

    mlflow.log_metric("loss", loss, step=epoch)
    mlflow.log_metric("accuracy", acc, step=epoch)
```

## Pipeline de Inferência Observável

### Métricas RED (Rate, Errors, Duration)

O padrão **RED** é o mínimo absoluto para qualquer serviço:

- **Rate**: Quantas requisições por segundo?
- **Errors**: Quantos erros por segundo?
- **Duration**: Quanto tempo cada requisição leva?

```python
from prometheus_client import Counter, Histogram

REQUEST_COUNT = Counter(
    'inference_requests_total',
    'Total de requisições de inferência',
    ['model_name', 'status']
)

REQUEST_LATENCY = Histogram(
    'inference_request_duration_seconds',
    'Latência de requisições de inferência',
    ['model_name'],
    buckets=[0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0, 2.5]
)
```

### Métricas Específicas de ML

Além do RED, adicione:

```python
PREDICTION_CONFIDENCE = Histogram(
    'prediction_confidence',
    'Distribuição de confiança das predições',
    ['model_name', 'predicted_class'],
    buckets=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99]
)

PREDICTION_CLASS_COUNT = Counter(
    'prediction_class_total',
    'Contagem de predições por classe',
    ['model_name', 'predicted_class']
)

FEATURE_VALUE = Histogram(
    'input_feature_value',
    'Distribuição dos valores de features de entrada',
    ['feature_name'],
    buckets=[0, 1, 2, 3, 4, 5, 6, 7, 8]  # ajustar para seu domínio
)
```

## Detecção de Data Drift

Data drift é detectado comparando a distribuição dos dados de entrada em produção com a distribuição dos dados de treino.

### Abordagem com Kolmogorov-Smirnov

```python
from scipy import stats
import numpy as np

def calculate_drift(reference_data, production_data, feature_name):
    """Calcula KS-statistic entre distribuições."""
    statistic, p_value = stats.ks_2samp(reference_data, production_data)
    return {
        'feature': feature_name,
        'ks_statistic': statistic,
        'p_value': p_value,
        'drift_detected': p_value < 0.05
    }
```

O resultado é exportado como métrica Prometheus para criar alertas automáticos quando drift é detectado.

## Padrão de Instrumentação

Todo componente deve seguir este padrão:

```
1. Definir métricas como constantes no módulo
2. Instrumentar a lógica de negócio (decorators ou context managers)
3. Expor endpoint /metrics (ou usar pushgateway para jobs batch)
4. Registrar no Prometheus (static config ou service discovery)
5. Criar painel no Grafana
6. Definir alerta para condições anômalas
```
