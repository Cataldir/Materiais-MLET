# Aula 03 - Grafana para ML com stack local

Pacote config-first para montar uma stack minima de observabilidade local com Prometheus e Grafana, sem exigir cloud ou servicos externos. O material acompanha um emissor deterministico de metricas para alimentar o dashboard com sinais tipicos de uma API de scoring.

## Objetivo didatico

- mostrar como Grafana entra na camada visual de monitoramento de modelos;
- fornecer uma stack local simples para dashboards, scraping e emissores de metricas;
- manter um artefato executavel que gere as metricas do exemplo sem rede externa.

## O que foi preservado

- `docker-compose.yml` para orquestrar a stack local;
- configuracao provisionada de datasource e dashboard;
- emissor Python deterministico de metricas em formato Prometheus.

## O que foi simplificado

- sem autenticao, alert manager ou persistencia longa;
- sem exporter dedicado ou API HTTP rodando continuamente;
- dashboard reduzido a poucos paineis suficientes para walkthrough e smoke test.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula03-grafana-ml
python emit_metrics.py
docker compose up
```

## Arquivos

- `emit_metrics.py`: gera metricas deterministicas e pode salvar uma amostra local.
- `docker-compose.yml`: sobe Prometheus e Grafana.
- `prometheus.yml`: faz scrape do emissor local de exemplo.
- `grafana/`: provisioning e dashboard versionado.

## Observacoes didaticas

- em ambiente de aula, o emissor pode ser executado periodicamente ou servir apenas como snapshot;
- o dashboard foi mantido simples para destacar latencia, drift score e taxa de erro;
- a pilha local ajuda a discutir topologia antes de integrar observabilidade real.