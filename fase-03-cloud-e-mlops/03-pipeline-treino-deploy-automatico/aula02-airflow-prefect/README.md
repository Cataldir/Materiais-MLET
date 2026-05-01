# Aula 02 - Orquestracao com Airflow e Prefect

Pacote canonico local com DAG Airflow que orquestra o ciclo completo de ML: preparacao de dados, treino, avaliacao e deploy condicional.

## Objetivo didatico

- criar um DAG Airflow com tasks encadeadas para pipeline de ML;
- implementar quality gate automatico baseado em metrica de avaliacao;
- configurar scheduling, retries e dependencias entre tasks.

## O que foi preservado

- DAG completo com 4 tasks: prepare, train, evaluate, deploy;
- quality gate que bloqueia deploy se AUC < threshold;
- configuracao realista com retry, scheduling semanal e logging.

## O que foi simplificado

- sem Docker Compose para Airflow (execucao via `airflow dags test`);
- treino simula geracao de metricas em vez de usar modelo real;
- sem XCom para passagem de artefatos entre tasks.

## Execucao

```bash
cd fase-03-cloud-e-mlops/03-pipeline-treino-deploy-automatico/aula02-airflow-prefect
pip install apache-airflow
airflow dags test ml_pipeline 2024-01-01
```

## Arquivos

- `ml_dag.py`: DAG Airflow com pipeline de ML completo (prepare → train → evaluate → deploy).

## Observacoes didaticas

- DAGs expressam dependencias como grafo, tornando o pipeline auditavel e reprodutivel;
- quality gates automaticos evitam deploy de modelos degradados;
- PythonOperator e o operador mais flexivel para tasks de ML personalizadas.
