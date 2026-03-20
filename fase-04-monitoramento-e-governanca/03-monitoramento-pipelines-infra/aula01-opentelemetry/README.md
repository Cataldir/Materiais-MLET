# Aula 01 - Tracing local inspirado em OpenTelemetry

Pacote canonico leve para explicar tracing ponta a ponta em pipelines de ML sem depender de collector remoto. A aula mostra como spans locais descrevem ingestao, transformacao e treino em uma trilha observavel e facil de depurar.

## Objetivo didatico

- explicar o que um span representa em um pipeline instrumentado;
- conectar etapas de pipeline a atributos observaveis e tempo de execucao;
- preparar o aluno para stacks mais completas de telemetria sem exigir backend externo.

## O que foi preservado

- nomenclatura de spans, atributos e resumo agregado;
- visao ponta a ponta de um pipeline pequeno;
- leitura executiva sobre duracao total e etapas mais relevantes.

## O que foi simplificado

- sem collector OTLP, Jaeger ou backend remoto como requisito;
- sem dependencia obrigatoria de OpenTelemetry no ambiente;
- foco no contrato de tracing, nao na instalacao da stack completa.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/aula01-opentelemetry
python otel_tracing.py
```

## Arquivos

- `otel_tracing.py`: cria spans locais e resume um trace de pipeline.
- `01_opentelemetry_local.ipynb`: notebook local com o mesmo fluxo do script.

## Observacoes didaticas

- a aula ensina o contrato do tracing antes do backend de observabilidade;
- spans pequenos e atributos legiveis facilitam live, estudo guiado e debugging local.