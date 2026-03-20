# Aula 06 - Pipeline de alertas para drift

Pacote canonico local para mostrar como um pipeline de monitoramento pode comparar uma base de referencia com janelas recentes de producao e emitir alertas por limiar sem depender de servicos externos. O material usa dados sinteticos tabulares e mantem o fluxo deterministico para aula, notebook e smoke tests.

## Objetivo didatico

- transformar comparacoes de distribuicao em um pipeline repetivel;
- classificar cada janela como `ok`, `warn` ou `alert` com base em thresholds simples;
- mostrar como um alerta pode ser explicado por feature em vez de um numero agregado opaco.

## O que foi preservado

- pipeline local executavel por script ou notebook;
- metricas leves por feature com KS aproximado e deslocamento medio;
- saida programatica em dataclasses para reaproveitar em testes e contratos locais.

## O que foi simplificado

- sem Prometheus, Evidently, NannyML ou qualquer backend remoto;
- sem persistencia historica entre execucoes;
- thresholds fixos para priorizar interpretacao pedagogica.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula06-pipeline-alertas
python drift_pipeline.py
```

## Arquivos

- `drift_pipeline.py`: executa o pipeline local, gera janelas sinteticas e classifica alertas por feature.
- `06_pipeline_alertas_local.ipynb`: notebook com a mesma sequencia principal para exploracao interativa.

## Observacoes didaticas

- `ok` indica que as features ficaram dentro do envelope esperado da referencia;
- `warn` indica degradacao moderada, util para acompanhamento manual;
- `alert` indica mudanca suficiente para acionar investigacao ou retraining orientado a regra local.