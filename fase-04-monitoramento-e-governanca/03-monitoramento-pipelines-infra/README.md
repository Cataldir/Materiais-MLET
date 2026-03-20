# 03 — Monitoramento de Pipelines e Infraestrutura

> 3h de vídeo · 3 aulas

## Por que esta disciplina importa

Nem todo problema em produção vem do modelo; muitos nascem no pipeline, na infraestrutura ou na ausência de resposta operacional. Esta disciplina amplia o monitoramento para além da predição, cobrindo tracing, uso de recursos e mecanismos de alerting que sustentam a confiabilidade do sistema.

## O que você deve aprender

- instrumentar pipelines com tracing e telemetria;
- observar recursos críticos como CPU, memória e GPU;
- configurar alertas e fluxos de resposta com AlertManager e práticas de on-call;
- distinguir sintomas de modelo de sintomas de infraestrutura.

## Como usar este material

1. Comece pelo tracing para entender visibilidade ponta a ponta.
2. Em seguida, observe métricas de infraestrutura e gargalos de recursos.
3. Use a aula de alerting para conectar monitoramento e ação.
4. Reutilize essa base quando analisar incidentes em pipelines maiores do curso.

## Como referenciar esta disciplina no repositório

- O caminho de referência é `fase-04-monitoramento-e-governanca/03-monitoramento-pipelines-infra/`.
- Cite a aula específica ao discutir tracing, métricas de recursos ou alerting.
- Este README explica o papel da disciplina; os arquivos de configuração e scripts mostram a prática operacional.
- A formalização de processos e evidências está fora desta pasta, na governança central.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, a disciplina reduz tempo de diagnóstico e melhora resiliência operacional. Academicamente, ela ajuda a analisar sistemas de ML como infraestrutura observável, aproximando teoria de confiabilidade e prática de telemetria aplicada.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-opentelemetry/) | OpenTelemetry para pipelines ML | `otel_tracing.py` |
| [02](aula02-metricas-infra/) | Métricas de infra (CPU, memória, GPU) | `docker-compose.yml` |
| [03](aula03-alerting/) | Alerting, on-call, AlertManager | `alertmanager.yml` |
