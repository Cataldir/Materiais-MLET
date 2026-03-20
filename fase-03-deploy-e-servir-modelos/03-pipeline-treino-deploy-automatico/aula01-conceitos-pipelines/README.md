# Aula 01 - Conceitos de pipelines

Pacote canonico local para representar um pipeline de ML como um DAG de metadados. O objetivo e explicar dependencia entre estagios sem acoplar o aluno a um orquestrador especifico.

## Objetivo didatico

- modelar etapas, dependencias e donos de cada fase do pipeline;
- validar ordenacao topologica localmente;
- reforcar que pipeline comeca pelo contrato dos estagios antes da ferramenta.

## O que foi preservado

- visao em DAG de treino e deploy;
- metadados de ownership e saidas por etapa;
- dependencia explicita entre estagios.

## O que foi simplificado

- sem Airflow, Prefect ou agentes externos;
- sem persistencia remota de artefatos;
- apenas grafo local com biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula01-conceitos-pipelines
python pipeline_metadata.py
```

## Arquivos

- `pipeline_metadata.py`: DAG local com validacao topologica e metadados de cada etapa.

## Observacoes didaticas

- a ferramenta de orquestracao vem depois do desenho do fluxo;
- ownership e saida esperada ajudam a reduzir ambiguidade operacional;
- dependencias explicitas sao um contrato util para CI, treino e deploy.