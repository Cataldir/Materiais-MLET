# Aula 03 - Alerting local para pipelines de ML

Pacote canonico leve para transformar metricas em incidentes acionaveis sem depender de Alertmanager real. A aula demonstra avaliacao por regras, cooldown para evitar ruido e um plano simples de notificacao por severidade.

## Objetivo didatico

- converter sinais de operacao em alertas com severidade explicita;
- evitar ruido com regras de cooldown e deduplicacao;
- associar cada alerta a uma resposta operacional minima.

## O que foi preservado

- leitura por severidade `warning` e `critical`;
- timeline de incidente com repeticao de snapshots;
- plano de notificacao orientado a resposta operacional.

## O que foi simplificado

- sem Slack, PagerDuty ou Alertmanager reais como requisito;
- sem integracao com webhooks externos;
- regras locais pequenas para facilitar debug e experimentacao.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula03-alerting
python alerting_demo.py
```

## Arquivos

- `alerting_demo.py`: avalia snapshots, aplica cooldown e monta o plano de notificacao.
- `03_alerting_local.ipynb`: notebook local com o mesmo fluxo do script.

## Observacoes didaticas

- alertas repetidos sem deduplicacao aumentam fadiga operacional;
- a aula mostra como sair de metrica bruta para acao recomendada.