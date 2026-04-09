# Plano de Aula — Monitoramento de Pipelines e Infraestrutura de ML

> **Duração**: 2 horas | **Formato**: Aula ao vivo com demonstrações práticas

---

## Objetivos de Aprendizagem

Ao final desta aula, o aluno será capaz de:

1. Explicar os três pilares da observabilidade (métricas, logs, traces) aplicados a sistemas de ML
2. Instrumentar pipelines de treino e inferência com Prometheus e MLflow
3. Construir dashboards operacionais no Grafana para monitorar modelos em produção
4. Configurar alertas para degradação de performance, drift e falhas de infraestrutura
5. Provisionar infraestrutura de monitoramento na Azure com Terraform

---

## Cronograma Detalhado

### Bloco 1 — Fundamentos de Observabilidade para ML (25 min)

| Tempo | Tópico | Tipo |
|---|---|---|
| 0:00–0:10 | Por que monitorar modelos de ML é diferente de monitorar software tradicional | Expositivo |
| 0:10–0:15 | Os três pilares: Métricas, Logs e Traces no contexto MLOps | Expositivo |
| 0:15–0:20 | Taxonomia de métricas: infra, modelo, dados, negócio | Expositivo + Diagrama |
| 0:20–0:25 | Mapa do stack: Prometheus + Grafana + MLflow — como se conectam | Expositivo + Arquitetura |

### Bloco 2 — Stack de Monitoramento na Prática (30 min)

| Tempo | Tópico | Tipo |
|---|---|---|
| 0:25–0:30 | Demo: Subindo o stack com Docker Compose | Live coding |
| 0:30–0:40 | Prometheus: modelo pull, PromQL básico, service discovery | Expositivo + Demo |
| 0:40–0:50 | Grafana: criação de dashboard, variáveis, painéis de séries temporais | Live coding |
| 0:50–0:55 | MLflow: experiment tracking, model registry, integração com métricas | Demo |

### Bloco 3 — Instrumentando Pipelines de ML (35 min)

| Tempo | Tópico | Tipo |
|---|---|---|
| 0:55–1:05 | Pipeline de treino observável: métricas de epoch, validação, duração | Live coding |
| 1:05–1:15 | Pipeline de inferência observável: latência, throughput, distribuição de predições | Live coding |
| 1:15–1:25 | Detecção de Data Drift com métricas Prometheus | Live coding |
| 1:25–1:30 | Alertas: definição de SLOs, regras no Prometheus, canais no Grafana | Demo |

### Bloco 4 — Infraestrutura e Produção (25 min)

| Tempo | Tópico | Tipo |
|---|---|---|
| 1:30–1:40 | Terraform para Azure: provisionando o stack de monitoramento | Walkthrough |
| 1:40–1:48 | Padrões de produção: retenção, escalabilidade, multi-tenant | Expositivo |
| 1:48–1:55 | Anti-patterns e armadilhas comuns | Expositivo |
| 1:55–2:00 | Recapitulação e próximos passos | Encerramento |

---

## Pré-requisitos do Aluno

- Docker e Docker Compose instalados
- Python 3.11+
- Conhecimento básico de scikit-learn e FastAPI
- (Desejável) Conta Azure com créditos acadêmicos

## Material de Apoio

- `docs/01-fundamentos.md` — Conceitos teóricos expandidos
- `docs/02-stack-prometheus-grafana.md` — Guia detalhado do stack
- `docs/03-mlflow-tracking.md` — MLflow tracking e registry
- `docs/04-pipelines-observaveis.md` — Instrumentação passo a passo
- `docs/05-infraestrutura-azure.md` — Deploy na Azure

## Exercícios Propostos

1. **Básico**: Adicionar uma métrica customizada ao pipeline de treino que registre o tamanho do dataset
2. **Intermediário**: Criar um painel Grafana que mostre a distribuição de confiança das predições
3. **Avançado**: Implementar alerta de concept drift comparando métricas de treino vs. inferência
4. **Desafio**: Estender o Terraform para provisionar o stack completo na Azure com Private Endpoints
