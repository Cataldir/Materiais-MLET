# Aula 04 - Pipeline end-to-end

Pacote canonico local para representar um pipeline completo de treino ate deploy com fronteiras de estagio explicitas. O material enfatiza o contrato entre etapas, e nao a ferramenta que orquestra o fluxo.

## Objetivo didatico

- separar entradas e saidas de cada fase do pipeline;
- demonstrar aprovacao de modelo antes do deploy;
- consolidar treino, validacao e empacotamento em um fluxo unico e local.

## O que foi preservado

- etapa de ingestao, feature building, treino, validacao e deploy;
- gate de qualidade antes da promocao;
- evidencias por estagio para depuracao e auditoria.

## O que foi simplificado

- sem orquestrador externo e sem ambiente remoto;
- sem datasets grandes ou modelagem estatistica pesada;
- simulacao totalmente deterministica com biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula04-pipeline-e2e
python e2e_pipeline.py
```

## Arquivos

- `e2e_pipeline.py`: pipeline end-to-end com contratos de fronteira por estagio.

## Observacoes didaticas

- fronteiras explicitas evitam que uma etapa conheca detalhes internos da outra;
- cada saida pode virar um artefato versionado em um pipeline real;
- o gate final ajuda a ligar treino, avaliacao e deploy continuo.