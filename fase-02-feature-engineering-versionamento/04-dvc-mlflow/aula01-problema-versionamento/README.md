# Aula 01 - Por que versionar dados e modelos

Pacote canonico leve para enquadrar o problema de rastreabilidade antes de introduzir DVC e MLflow. A aula mostra como datasets, parametros e artefatos sem versao tornam resultados dificeis de auditar, reproduzir e defender em ambientes de negocio.

## Objetivo didatico

- evidenciar por que reproducao sem metadados confiaveis falha rapidamente;
- conectar versionamento a auditabilidade, rollback e confianca operacional;
- preparar a leitura das ferramentas a partir de uma dor concreta.

## O que foi preservado

- comparacao entre execucoes com e sem identificadores de dataset e modelo;
- linguagem proxima de experimentacao, release e investigacao de incidente;
- foco no valor pratico do historico antes do detalhe da ferramenta.

## O que foi simplificado

- sem dependencia de DVC, MLflow ou storage remoto para abrir o pack;
- sem pipeline real de treino e sem registry externo;
- exemplos pequenos para facilitar discussao e reproducao local.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula01-problema-versionamento
python versioning_problem.py
```

## Arquivos

- `versioning_problem.py`: compara runs versionados e nao versionados e destaca o impacto na reproducao.
- `01_problema_versionamento_local.ipynb`: notebook local para discutir auditabilidade e rollback.

## Observacoes didaticas

- o argumento principal nao e burocracia, e sim capacidade de explicar por que um resultado aconteceu;
- a ferramenta entra depois que a necessidade de rastreio ficou clara.