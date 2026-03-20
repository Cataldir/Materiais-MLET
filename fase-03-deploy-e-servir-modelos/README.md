# Fase 03 — Deploy e Servir Modelos

> ~23h de vídeo · 6 disciplinas · ~19 aulas

## Por que esta fase importa

É aqui que o estudante deixa de pensar apenas em treinamento e passa a operar sistemas de ML como produto. A fase trata do caminho entre um modelo validado e um serviço com deploy, automação, observabilidade e controle de desempenho, incluindo cenários de dados não estruturados e exigências de latência.

## Ao concluir esta fase, você deve ser capaz de

- comparar estratégias de deploy em nuvem e selecionar a mais adequada ao caso de uso;
- implementar pipelines de CI/CD para ativos de ML;
- automatizar etapas de treino, avaliação e publicação de modelos;
- monitorar performance operacional e técnica do serviço exposto;
- identificar gargalos de latência e throughput em workloads mais pesados.

## Relação com o Tech Challenge

O Tech Challenge desta etapa exige que a solução deixe de ser somente correta em ambiente local e passe a ser operável. Esta fase prepara o aluno para demonstrar entrega fim a fim: pipeline, automação, serving, monitoramento e decisões explícitas de arquitetura operacional.

## Como navegar nesta fase

1. Abra Deploy em Nuvem para entender os padrões de publicação.
2. Passe por CI/CD e Pipeline Automático para amarrar automação e release.
3. Use Monitoração de Performance e Serviços de Monitoração para observar o sistema em execução.
4. Feche com Latência e Performance para trabalhar restrições reais de produção.
5. As regras de material executável continuam no [Guia 007](../../../governanca/04-guias/07-guia-de-materiais-tecnico-pedagogicos-executaveis.md), enquanto critérios de avaliação e contexto de desafio estão no [Resumo dos Tech Challenges](../../../governanca/resumo-tech-challenges.md).

## Disciplinas

| # | Nome | Papel na fase | Aulas |
|---|------|---------------|-------|
| [01](01-deploy-em-nuvem/README.md) | Deploy em Nuvem | comparar plataformas e padrões de publicação | 3 |
| [02](02-integracao-cicd/README.md) | Integração com CI/CD | automatizar verificação e entrega | 5 |
| [03](03-pipeline-treino-deploy-automatico/README.md) | Pipeline de Treino e Deploy Automático | orquestrar o fluxo ponta a ponta | 4 |
| [04](04-monitoracao-performance/README.md) | Monitoração de Performance | medir comportamento operacional do serviço | 4 |
| [05](05-servicos-de-monitoracao/README.md) | Serviços de Monitoração | comparar stacks e serviços de observabilidade | 3 |
| [06](06-latencia-performance/README.md) | Latência e Performance — Dados Não Estruturados | otimizar workloads pesados | 4 |

## Como usar o material da fase

- Use os READMEs das disciplinas para escolher o nível de profundidade necessário.
- Prefira executar primeiro exemplos mínimos e depois os fluxos integradores.
- Recorra aos pacotes de referência quando precisar de benchmark adicional ou inspiração arquitetural.

## Setup

```bash
make install-fase03
# ou
uv pip install -e ".[fase03,dev]"
```
