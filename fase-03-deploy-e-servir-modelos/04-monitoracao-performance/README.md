# 04 — Monitoração de Performance

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Depois do deploy, a pergunta deixa de ser “funciona?” e passa a ser “como está se comportando ao longo do tempo?”. Esta disciplina introduz métricas, dashboards e alertas para observar o desempenho de modelos e APIs em produção.

## O que você deve aprender

- definir métricas úteis para serviços de ML em operação;
- instrumentar aplicações com Prometheus e Grafana;
- configurar regras de alerta e sinais de anomalia;
- consolidar uma visão de monitoramento que suporte tomada de decisão.

## Como usar este material

1. Comece pela coleta de métricas para entender o que vale medir.
2. Em seguida, reproduza a stack com Prometheus e Grafana.
3. Use a aula de alertas para pensar resposta operacional, não só visualização.
4. Feche no projeto consolidado para observar a disciplina como sistema integrado.

## Como referenciar esta disciplina no repositório

- O caminho da trilha é `fase-03-deploy-e-servir-modelos/04-monitoracao-performance/`.
- Cite a aula e o artefato correspondente quando precisar mostrar instrumentação, dashboard ou alerta.
- O README resume intenção e navegação; configurações, notebooks e scripts são a prova executável.
- Regras de avaliação e processos institucionais não são mantidas nesta pasta.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Em ambientes reais, observabilidade é pré-condição para SLA, custo controlado e resposta a incidentes. No plano acadêmico, a disciplina ajuda a operacionalizar conceitos de medição, monitoramento e anomalia com evidência concreta e reproduzível.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-metricas-producao/) | Métricas de modelo em produção | `collect_metrics.py` |
| [02](aula02-prometheus-grafana/) | Prometheus + Grafana + FastAPI instrumentada | `README.md`, `api_instrumented.py`, `docker-compose.yml`, `prometheus.yml`, notebook |
| [03](aula03-alertas/) | Alertas, anomaly detection | `alert_rules.yml`, `anomaly_detection.py` |
| [04](aula04-projeto-monitoramento/) | Projeto de monitoramento consolidado | notebook |
