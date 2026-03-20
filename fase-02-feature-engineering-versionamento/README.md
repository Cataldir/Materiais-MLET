# Fase 02 — Feature Engineering e Versionamento

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
5. Quando houver dúvida sobre padrão de material ou referencial, consulte o [Guia 007](../../../governanca/04-guias/07-guia-de-materiais-tecnico-pedagogicos-executaveis.md) e o [Guia 008](../../../governanca/04-guias/08-guia-de-referenciais-teoricos-por-disciplina.md).

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

## Setup

```bash
make install-fase02
# ou
uv pip install -e ".[fase02,dev]"
```
