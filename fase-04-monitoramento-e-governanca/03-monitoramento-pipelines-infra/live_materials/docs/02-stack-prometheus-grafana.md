# Stack de Monitoramento: Prometheus + Grafana

## Prometheus — Modelo de Coleta Pull

Prometheus funciona com um modelo **pull**: ele faz scrape de endpoints `/metrics` dos seus serviços em intervalos regulares (tipicamente 15s).

### Tipos de Métricas

| Tipo | Uso | Exemplo |
|---|---|---|
| **Counter** | Valores que só crescem | Total de predições, total de erros |
| **Gauge** | Valores que sobem e descem | Uso de memória, modelos carregados |
| **Histogram** | Distribuição de valores | Latência de inferência |
| **Summary** | Percentis pré-calculados | P50, P95, P99 de latência |

### PromQL — Linguagem de Consulta

```promql
# Taxa de requisições por segundo (últimos 5 minutos)
rate(prediction_requests_total[5m])

# Latência P99 de inferência
histogram_quantile(0.99, rate(prediction_latency_seconds_bucket[5m]))

# Proporção de erros
rate(prediction_errors_total[5m]) / rate(prediction_requests_total[5m])

# Drift score médio por feature
avg by (feature_name) (feature_drift_score)

# Throughput de treino (samples/segundo)
rate(training_samples_processed_total[1m])
```

### Service Discovery

Em ambiente Docker, o Prometheus descobre serviços via:

1. **Static configs** (simples, usado nesta aula)
2. **DNS-based** (Docker Compose network)
3. **Kubernetes SD** (produção)
4. **Azure SD** (via Azure Monitor)

## Grafana — Visualização e Alertas

### Conceitos Principais

- **Datasource**: conexão com Prometheus (ou outros backends)
- **Dashboard**: coleção de painéis organizados
- **Panel**: visualização individual (gráfico, gauge, tabela)
- **Variable**: parâmetros dinâmicos (ex: selecionar modelo, ambiente)
- **Alert rule**: condição que dispara notificação

### Tipos de Painel Recomendados para ML

| Painel | Uso |
|---|---|
| **Time series** | Latência, throughput, accuracy ao longo do tempo |
| **Stat** | Valor atual de métricas-chave (uptime, modelo ativo) |
| **Gauge** | Utilização de recursos (CPU, memória, GPU) |
| **Heatmap** | Distribuição de latência por hora/dia |
| **Table** | Lista de alertas ativos, modelos registrados |
| **Bar gauge** | Comparação de drift entre features |

### Alertas no Grafana

```yaml
# Exemplo de alerta: latência P99 > 500ms por 5 minutos
- alert: HighInferenceLatency
  expr: histogram_quantile(0.99, rate(prediction_latency_seconds_bucket[5m])) > 0.5
  for: 5m
  labels:
    severity: warning
  annotations:
    summary: "Latência de inferência elevada"
    description: "P99 de latência está em {{ $value }}s"
```

## Integrando Prometheus com Python

A biblioteca `prometheus_client` fornece instrumentação nativa:

```python
from prometheus_client import Counter, Histogram, Gauge, start_http_server

# Definir métricas
PREDICTIONS = Counter(
    'prediction_requests_total',
    'Total de requisições de predição',
    ['model_name', 'model_version']
)

LATENCY = Histogram(
    'prediction_latency_seconds',
    'Latência de inferência em segundos',
    buckets=[0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0]
)

MODEL_LOADED = Gauge(
    'model_loaded_info',
    'Informações do modelo carregado',
    ['model_name', 'model_version']
)

# Expor métricas na porta 8001
start_http_server(8001)
```

Cada chamada de `PREDICTIONS.labels(model_name="iris", model_version="v3").inc()` incrementa o counter, e o Prometheus faz scrape periodicamente.
