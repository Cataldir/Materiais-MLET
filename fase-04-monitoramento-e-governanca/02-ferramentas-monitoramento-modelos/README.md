# 02 — Ferramentas de Monitoramento de Modelos

> 3h de vídeo · 3 aulas

## Por que esta disciplina importa

Depois de entender por que monitorar, é preciso conhecer ferramentas concretas que tornem isso viável. Esta disciplina apresenta stacks e bibliotecas que ajudam a transformar sinais de produção em perfis, dashboards e acompanhamento contínuo do comportamento do modelo.

## O que você deve aprender

- usar ferramentas de profiling e observação como whylogs;
- integrar rastreamento contínuo com MLflow em contexto de monitoramento;
- montar dashboards de apoio com Grafana;
- comparar o papel de cada ferramenta dentro de uma arquitetura de monitoramento.

## Como usar este material

1. Comece por whylogs para entender profiling de produção.
2. Em seguida, veja como o MLflow pode participar de uma esteira contínua de monitoramento.
3. Use a aula de Grafana para enxergar a dimensão visual e operacional do acompanhamento.
4. Recombine essas peças com Data Drift e Monitoramento de Pipelines para montar uma visão integrada.

## Como referenciar esta disciplina no repositório

- O caminho principal é `fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/`.
- Cite a ferramenta e a aula correspondente quando precisar apontar um exemplo concreto.
- O README contextualiza uso e comparação; os scripts e stacks demonstram a aplicação prática.
- A camada normativa continua centralizada na governança do repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática profissional, escolher bem as ferramentas reduz tempo de observação, melhora diagnóstico e evita monitoramento superficial. Academicamente, a disciplina ajuda a distinguir conceito de implementação e permite analisar limites, cobertura e custo de diferentes estratégias instrumentadas.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-whylogs/) | whylogs: profiling em produção | `whylogs_profiling.py` |
| [02](aula02-mlflow-monitoramento/) | MLflow para monitoramento contínuo | `mlflow_monitoring.py` |
| [03](aula03-grafana-ml/) | Dashboards Grafana para ML | `docker-compose.yml` |
