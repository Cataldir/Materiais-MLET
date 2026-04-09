# Fundamentos de Observabilidade para Machine Learning

## Por Que ML é Diferente?

Software tradicional falha de forma **binária** — funciona ou não funciona. Modelos de ML falham de forma **gradual e silenciosa**. Um modelo pode continuar retornando respostas HTTP 200 enquanto suas predições se degradam sem que ninguém perceba.

Essa degradação silenciosa acontece por múltiplas razões:

- **Data drift**: a distribuição dos dados de entrada muda ao longo do tempo
- **Concept drift**: a relação entre features e target muda
- **Degradação de infraestrutura**: latência crescente, memory leaks, saturação de GPU
- **Stale models**: modelo treinado com dados de 6 meses atrás servindo dados de hoje

## Os Três Pilares da Observabilidade

```
┌─────────────────────────────────────────────────┐
│              OBSERVABILIDADE                    │
├─────────────────┬──────────────┬────────────────┤
│    MÉTRICAS     │    LOGS      │    TRACES      │
│  (Prometheus)   │  (stdout/    │ (OpenTelemetry │
│                 │   ELK/Loki)  │  / Jaeger)     │
├─────────────────┼──────────────┼────────────────┤
│ • Latência P99  │ • Erros de   │ • Fluxo de um  │
│ • Throughput    │   predição   │   request      │
│ • Accuracy      │ • Stack      │ • Gargalos     │
│ • Drift score   │   traces     │   entre        │
│ • GPU util      │ • Data       │   serviços     │
│                 │   warnings   │                │
└─────────────────┴──────────────┴────────────────┘
```

### Métricas (foco desta aula)

Valores numéricos agregados ao longo do tempo. São o pilar mais importante para monitoramento contínuo porque:

- São **baratos** de armazenar (séries temporais compactas)
- Permitem **alertas automáticos** via thresholds
- São **queryáveis** com PromQL para análise ad-hoc

### Logs

Registros textuais de eventos discretos. Complementam métricas com contexto detalhado quando algo dá errado.

### Traces

Rastreamento de requisições end-to-end através de múltiplos serviços. Essenciais em arquiteturas de microserviços.

## Taxonomia de Métricas para ML

### 1. Métricas de Infraestrutura

| Métrica | Descrição | Alerta típico |
|---|---|---|
| `cpu_usage_percent` | Utilização de CPU do serviço | > 80% por 5 min |
| `memory_usage_bytes` | Consumo de memória | > 90% do limite |
| `gpu_utilization` | Utilização da GPU (treino) | < 30% (subutilização) |
| `disk_io_bytes` | I/O de disco | Latência > 100ms |

### 2. Métricas de Modelo

| Métrica | Descrição | Alerta típico |
|---|---|---|
| `prediction_latency_seconds` | Tempo de inferência | P99 > 200ms |
| `prediction_throughput` | Predições por segundo | < threshold mínimo |
| `model_accuracy` | Acurácia em produção | Queda > 5% |
| `prediction_confidence` | Distribuição de confiança | Média < 0.7 |

### 3. Métricas de Dados

| Métrica | Descrição | Alerta típico |
|---|---|---|
| `feature_drift_score` | KS-test entre treino e prod | Score > 0.1 |
| `missing_values_ratio` | Percentual de nulos | > 5% |
| `input_distribution_mean` | Média das features | Desvio > 2σ do baseline |
| `data_freshness_seconds` | Idade dos dados | > 24h |

### 4. Métricas de Negócio

| Métrica | Descrição | Alerta típico |
|---|---|---|
| `conversion_rate` | Taxa de conversão | Queda > 10% |
| `false_positive_rate` | Taxa de falsos positivos | > threshold regulatório |
| `revenue_impact` | Impacto financeiro estimado | Negativo por 1h |

## Arquitetura de Referência

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│  Training    │     │  Inference   │     │  Data        │
│  Pipeline    │     │  Service     │     │  Pipeline    │
│  (Python)    │     │  (FastAPI)   │     │  (Airflow)   │
└──────┬───────┘     └──────┬───────┘     └──────┬───────┘
       │                    │                    │
       │  /metrics          │  /metrics          │  /metrics
       ▼                    ▼                    ▼
┌─────────────────────────────────────────────────────────┐
│                    PROMETHEUS                           │
│            (scrape, store, query, alert)                │
└───────────────────────┬─────────────────────────────────┘
                        │
           ┌────────────┼────────────┐
           ▼            ▼            ▼
     ┌──────────┐ ┌──────────┐ ┌──────────┐
     │ Grafana  │ │ Alert-   │ │ PromQL   │
     │ Dash-    │ │ manager  │ │ Queries  │
     │ boards   │ │ (PagerD.)│ │ (ad-hoc) │
     └──────────┘ └──────────┘ └──────────┘

┌─────────────────────────────────────────────────────────┐
│                      MLFLOW                             │
│         (experiment tracking, model registry,           │
│          artifact store, model lineage)                 │
└─────────────────────────────────────────────────────────┘
```

Prometheus cuida do **"como está agora"** (métricas operacionais em tempo real), enquanto MLflow cuida do **"como chegamos aqui"** (linhagem de experimentos, comparação de versões, reprodutibilidade). Juntos, formam a base de um sistema de ML observável.
