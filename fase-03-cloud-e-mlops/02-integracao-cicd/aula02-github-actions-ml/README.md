# Aula 02 - GitHub Actions para ML

Pacote canonico local com workflows de treino e deploy de modelos via GitHub Actions. Os arquivos YAML definem pipelines de CI/CD completos para projetos de Machine Learning.

## Objetivo didatico

- configurar workflows GitHub Actions para treino automatizado de modelos;
- integrar DVC e MLflow no pipeline de CI;
- implementar deploy condicional com quality gates e environment protection.

## O que foi preservado

- workflow de treino com DVC pull, MLflow tracking e upload de artefatos;
- workflow de deploy com quality gate, environment protection e health check;
- trigger por push em paths de dados/codigo e workflow_dispatch manual.

## O que foi simplificado

- sem runner self-hosted ou GPU;
- sem registry de containers (foco em workflow YAML);
- endpoints de deploy e health check sao placeholders.

## Execucao

Os workflows devem ser colocados em `.github/workflows/` de um repositorio GitHub para execucao automatica. Para estudo local, analise os arquivos YAML diretamente.

## Arquivos

- `.github/workflows/ml-train.yml`: workflow de treino com DVC + MLflow + artefatos.
- `.github/workflows/ml-deploy.yml`: workflow de deploy com quality gate e environment protection.

## Observacoes didaticas

- workflows de ML diferem dos tradicionais por incluir etapas de dados (DVC) e experimentos (MLflow);
- quality gates impedem deploy de modelos que nao atingem metricas minimas;
- environment protection rules permitem aprovacao manual antes de deploy em producao.
