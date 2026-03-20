# Aula 02 - Metricas de infraestrutura para pipelines de ML

Pacote canonico leve para relacionar consumo de CPU, memoria e latencia de pipeline com gargalos operacionais. A aula usa uma linha do tempo sintetica para manter a execucao local e tornar visivel quando a infraestrutura passa a explicar o incidente.

## Objetivo didatico

- observar sinais de saturacao de infraestrutura em um pipeline local;
- resumir capacidade, picos e gargalos em um relatorio simples;
- distinguir problema de modelo de problema de recurso computacional.

## O que foi preservado

- correlacao entre CPU, memoria e latencia percebida;
- leitura de gargalos por janelas sucessivas de execucao;
- resumo executivo de capacidade e risco operacional.

## O que foi simplificado

- sem Prometheus, Docker ou GPU real como caminho default;
- sem coleta real do host local para evitar variacao nao controlada;
- timeline sintetica deterministica para facilitar smoke tests e notebooks.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula02-metricas-infra
python infra_metrics.py
```

## Arquivos

- `infra_metrics.py`: gera uma timeline sintetica de recursos e identifica gargalos.
- `02_metricas_infra_local.ipynb`: notebook local com o mesmo fluxo do script.

## Observacoes didaticas

- a aula prioriza leitura operacional do incidente, nao fidelidade de coleta ao host;
- picos de CPU e memoria devem ser interpretados junto com a latencia observada.