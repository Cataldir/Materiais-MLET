# Monitoramento de Pipelines e Infraestrutura de ML

> **Pós-Tech em Engenharia de Machine Learning** — Aula ao vivo (2h)

## Visão Geral

Este repositório contém todo o material da aula **"Monitoramento de Pipelines e Infraestrutura"**, incluindo slides conceituais (em Markdown), código-fonte funcional, infraestrutura como código (Terraform + Docker Compose) e dashboards pré-configurados.

O objetivo é que o aluno saia da aula com um stack de observabilidade rodando localmente e saiba replicá-lo em ambiente cloud (Azure).

## Stack Tecnológico

| Componente | Papel |
|---|---|
| **Prometheus** | Coleta e armazenamento de métricas de séries temporais |
| **Grafana** | Visualização, dashboards e alertas |
| **MLflow** | Tracking de experimentos, registro de modelos e artefatos |
| **FastAPI** | Serviço de inferência com métricas instrumentadas |
| **Scikit-learn** | Pipeline de treinamento demonstrativo |
| **Docker Compose** | Orquestração local de todos os serviços |
| **Terraform** | Provisionamento na Azure (AKS, Azure Monitor, Container Apps) |

## Estrutura do Repositório

```
monitoramento_mlet/
├── README.md                          # Este arquivo
├── docs/
│   ├── 00-plano-de-aula.md           # Plano detalhado da aula (2h)
│   ├── 01-fundamentos.md             # Conceitos de observabilidade para ML
│   ├── 02-stack-prometheus-grafana.md # Deep-dive no stack de monitoramento
│   ├── 03-mlflow-tracking.md         # MLflow para tracking e registry
│   ├── 04-pipelines-observaveis.md   # Instrumentação de treino e inferência
│   └── 05-infraestrutura-azure.md    # Deploy na Azure com Terraform
├── src/
│   ├── common/
│   │   ├── __init__.py
│   │   ├── metrics.py                # Métricas Prometheus compartilhadas
│   │   └── config.py                 # Configuração centralizada
│   ├── training_pipeline/
│   │   ├── __init__.py
│   │   ├── train.py                  # Pipeline de treino com MLflow + Prometheus
│   │   ├── data_validation.py        # Validação de dados com métricas
│   │   └── drift_detector.py         # Detecção de data drift
│   ├── inference_pipeline/
│   │   ├── __init__.py
│   │   ├── app.py                    # API FastAPI instrumentada
│   │   ├── model_loader.py           # Carregamento de modelo do MLflow Registry
│   │   └── middleware.py             # Middleware de métricas
│   └── monitoring/
│       ├── __init__.py
│       ├── alerts.py                 # Definição de alertas programáticos
│       └── health_check.py           # Health checks compostos
├── infra/
│   ├── docker/
│   │   ├── docker-compose.yml        # Stack completo local
│   │   ├── Dockerfile.training       # Imagem do pipeline de treino
│   │   └── Dockerfile.inference      # Imagem do serviço de inferência
│   ├── prometheus/
│   │   ├── prometheus.yml            # Configuração do Prometheus
│   │   └── alert_rules.yml           # Regras de alerta
│   ├── grafana/
│   │   ├── provisioning/
│   │   │   ├── dashboards/
│   │   │   │   └── dashboards.yml    # Auto-provisioning config
│   │   │   └── datasources/
│   │   │       └── datasources.yml   # Prometheus datasource
│   │   └── dashboards/
│   │       └── ml-pipeline.json      # Dashboard principal
│   └── terraform/
│       ├── main.tf                   # Recursos Azure
│       ├── variables.tf              # Variáveis
│       ├── outputs.tf                # Outputs
│       └── providers.tf              # Provider config
├── notebooks/
│   └── exploratory_monitoring.ipynb  # Notebook demonstrativo
├── requirements.txt                  # Dependências Python
└── Makefile                          # Atalhos de execução
```

## Início Rápido

### Pré-requisitos

- Docker e Docker Compose v2+
- Python 3.11+
- (Opcional) Terraform 1.5+ e Azure CLI para deploy cloud

### Subir o stack local

```bash
# Clone e entre no diretório
cd monitoramento_mlet

# Suba todos os serviços
make up

# Ou diretamente:
docker compose -f infra/docker/docker-compose.yml up --build -d
```

### Acessar os serviços

| Serviço | URL |
|---|---|
| **Grafana** | http://localhost:3000 (admin / admin) |
| **Prometheus** | http://localhost:9090 |
| **MLflow** | http://localhost:5000 |
| **API de Inferência** | http://localhost:8000/docs |

### Executar o pipeline de treino

```bash
# Com Python local
pip install -r requirements.txt
python -m src.training_pipeline.train

# Ou via Docker
docker compose -f infra/docker/docker-compose.yml run training
```

### Testar a API de inferência

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"features": [5.1, 3.5, 1.4, 0.2]}'
```

## Licença

Material educacional — uso livre para fins acadêmicos.
