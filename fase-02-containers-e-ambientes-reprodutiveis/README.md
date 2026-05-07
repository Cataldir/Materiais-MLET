# Fase 02 — Containers e Ambientes Reprodutíveis

> ~18h de vídeo · 4 disciplinas · ~20 aulas

## Por que esta fase importa

Depois de aprender a modelar, o próximo salto profissional é garantir que o trabalho possa ser repetido, auditado e transportado entre pessoas e ambientes. Esta fase mostra que boa engenharia de ML depende tanto de features e dados quanto de disciplina operacional: código legível, ambientes reprodutíveis, conteinerização e rastreabilidade de artefatos.

## Ao concluir esta fase, você deve ser capaz de

- refatorar pipelines e scripts de ML com padrões de qualidade mais robustos;
- controlar dependências e ambientes para reduzir efeito de “funciona só na minha máquina”;
- empacotar serviços e jobs em contêineres adequados a desenvolvimento e deploy;
- versionar dados, modelos e experimentos com DVC e MLflow;
- preparar a base que permite CI/CD e deploy confiáveis na fase seguinte.

## Relação com o Tech Challenge

O Tech Challenge deixa de ser apenas uma solução correta e passa a exigir uma solução sustentável. Esta fase prepara o aluno para entregar projetos cujo código, ambiente, dados e modelos possam ser reconstruídos e avaliados sem depender de memória tácita do autor.

## Como navegar nesta fase

1. Comece por Clean Code para elevar a qualidade estrutural do código.
2. Em seguida, consolide ambientes com Gerenciamento de Dependências.
3. Use Docker e Kubernetes para materializar portabilidade e empacotamento.
4. Feche com DVC e MLflow para rastrear a linha de produção de dados, modelos e métricas.
5. Consulte os documentos em [docs](../docs/) para navegação, cobertura por turma e histórico editorial deste repositório.

## Disciplinas

| # | Nome | Papel na fase | Aulas |
|---|------|---------------|-------|
| [01](01-clean-code-ml/README.md) | Clean Code para Engenharia de ML | reduzir acoplamento e fragilidade estrutural | 4 |
| [02](02-gerenciamento-dependencias/README.md) | Gerenciamento de Dependências em ML | garantir reprodutibilidade de ambiente | 4 |
| [03](03-docker-kubernetes/README.md) | Docker e Kubernetes | empacotar e orquestrar workloads de ML | 5 |
| [04](04-dvc-mlflow/README.md) | Controle de Dados e Modelos — DVC + MLflow | versionar ativos críticos da solução | 7 |

## Como usar o material da fase

- Leia o README da disciplina antes de abrir aulas isoladas.
- Execute os artefatos localmente para entender o fluxo mínimo reproduzível.
- Trate os pacotes de referência como complementos para aprofundamento, não como substitutos do percurso principal.

## Material de apoio da fase

- [Grupos de estudo](grupos-de-estudo/README.md)
- [Live: Gerenciamento de Dependências em ML](02-gerenciamento-dependencias/lives/fase02-live-gerenciamento-de-dependencias-em-ml/README.md)
- [Live: Docker e Kubernetes](03-docker-kubernetes/lives/fase02-live-docker-e-kubernetes/README.md)
- [Live: Controle de Dados e Modelos — DVC e MLflow](04-dvc-mlflow/lives/fase02-live-controle-de-dados-e-modelos-dvc-e-mlflow/README.md)

## Setup

Quando precisar executar código desta fase, instale as dependências da fase a partir da raiz do repositório.

```bash
python -m pip install -r constraints/fase02.txt
```
