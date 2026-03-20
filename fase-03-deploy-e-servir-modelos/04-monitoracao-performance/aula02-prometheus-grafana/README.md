# Aula 02 - Prometheus e Grafana para APIs de ML

Pacote canonico local para observar uma API de inferencia com metricas de negocio e latencia expostas em formato Prometheus. O material preserva a stack existente com FastAPI, `docker-compose.yml` e `prometheus.yml`, e adiciona README e notebook para explicar o fluxo ponta a ponta.

## Objetivo didatico

- diferenciar metricas de negocio, latencia e health check em uma API de ML;
- mostrar como Prometheus faz scrape do endpoint `/metrics`;
- usar Grafana como camada de visualizacao sem alterar o comportamento da API.

## O que foi preservado

- endpoint `/predict` com contadores, histograma de latencia e distribuicao de confianca;
- `docker-compose.yml` e `prometheus.yml` como stack local de observabilidade;
- comportamento atual da API instrumentada.

## O que foi simplificado

- sem autenticacao, tracing distribuido ou alert manager;
- sem carga sintetica automatica dentro do pack;
- foco em instrumentacao local e funcoes testaveis para o notebook e smoke tests.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula02-prometheus-grafana
uvicorn api_instrumented:app --host 0.0.0.0 --port 8000
```

## Stack opcional

```bash
docker compose up --build
```

## Arquivos

- `api_instrumented.py`: API FastAPI com metricas Prometheus e funcao de scoring reutilizavel.
- `docker-compose.yml`: sobe API, Prometheus e Grafana localmente.
- `prometheus.yml`: define o scrape do endpoint `/metrics`.
- `02_prometheus_grafana_local.ipynb`: notebook para exercitar o scoring e discutir as metricas expostas.

## Observacoes didaticas

- o endpoint `/metrics` exporta telemetria para scraping; ele nao substitui logs de negocio;
- o contador de predicoes pode ser fatiado por classe prevista e status;
- transformar o core de scoring em funcao testavel ajuda a validar instrumentacao sem subir a API completa.