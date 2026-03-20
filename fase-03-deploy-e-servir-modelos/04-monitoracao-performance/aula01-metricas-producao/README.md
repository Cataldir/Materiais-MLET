# Aula 01 - Metricas de producao

Pacote canonico local para observar uma janela de inferencias em producao com coletores desacoplados. O fluxo usa um hub simples de eventos no estilo observer.

## Objetivo didatico

- distinguir latencia, erro e confianca como sinais de operacao;
- desacoplar coleta de metricas da emissao dos eventos;
- consolidar uma janela resumida de saude do sistema de inferencia.

## O que foi preservado

- telemetria por evento;
- agregacao por janela operacional;
- separacao entre emissor e coletores.

## O que foi simplificado

- sem Prometheus, OpenTelemetry ou banco temporal;
- sem rede, API ou dependencia externa;
- apenas simulacao local deterministica.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula01-metricas-producao
python production_metrics.py
```

## Arquivos

- `production_metrics.py`: telemetria local de producao com coletores desacoplados.

## Observacoes didaticas

- observer ajuda a adicionar metricas sem alterar o emissor principal;
- janelas pequenas facilitam analise e testes;
- o mesmo padrao pode ser ligado a exporters reais depois.