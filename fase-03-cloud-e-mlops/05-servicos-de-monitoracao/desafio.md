# Desafio — Serviços de Monitoração

> **Tipo:** Individual · Não obrigatório · Sem nota
> **Limite:** 2 páginas (≈ 1 000 palavras)

---

## 1. Contexto

Uma empresa de e-commerce tem 3 modelos em produção (recomendação, fraude, pricing), mas nenhum deles é monitorado além de health checks básicos. O CTO pede um **stack de observabilidade** com Prometheus + Grafana que cubra métricas de infra e de modelo. O aluno deve instrumentar um serviço de inferência e construir o dashboard.

## 2. Objetivos de Aprendizagem

| # | Objetivo |
|---|----------|
| O1 | Instrumentar API de inferência com `prometheus_client`. |
| O2 | Construir dashboard Grafana com ≥ 6 painéis (infra + modelo). |
| O3 | Configurar alertas baseados em PromQL. |
| O4 | Elaborar plano de observabilidade (métricas, logs, traces). |

## 3. Escopo e Limites

- **Inclui:** Instrumentação, Prometheus, Grafana, alertas.
- **Exclui:** Azure Monitor / CloudWatch (tema da própria aula, não do desafio principal).

## 4. Requisitos

### Funcionais (RF)
| RF | Descrição |
|----|-----------|
| RF-01 | Endpoint `/metrics` com ≥ 4 métricas: `request_count`, `prediction_latency`, `prediction_class`, `model_version`. |
| RF-02 | Dashboard Grafana com ≥ 6 painéis cobrindo infra + modelo. |
| RF-03 | ≥ 1 alerta configurado (ex.: latência P95 > threshold). |

### Não Funcionais (RNF)
| RNF | Descrição |
|-----|-----------|
| RNF-01 | Stack subido via Docker Compose (API + Prometheus + Grafana). |
| RNF-02 | Dashboard exportável como JSON. |

## 5. Passo a Passo (4 etapas)

| Etapa | Ação | Referência |
|-------|------|-----------|
| 1 | Elaborar plano de observabilidade (métricas por categoria). | Aula 01 |
| 2 | Instrumentar FastAPI com `prometheus_client` + expor `/metrics`. | Aula 02 |
| 3 | Docker Compose: API + Prometheus + Grafana. Criar dashboard com ≥ 6 painéis. | Aula 03 |
| 4 | Configurar alerta em Grafana e testar com carga (locust). | Aula 03, Aula 04 |

## 6. Entregáveis

| # | Artefato | Formato |
|---|---------|---------|
| E1 | Docker Compose completo | `docker-compose.yml` |
| E2 | Dashboard Grafana | JSON export |
| E3 | Plano de observabilidade | Markdown |

## 7. Checklist de Validação

- [ ] API expõe `/metrics` com ≥ 4 métricas.
- [ ] Prometheus scrape config aponta para API.
- [ ] Dashboard com ≥ 6 painéis (latência, throughput, CPU, prediction dist., etc.).
- [ ] ≥ 1 alerta funcional em Grafana.
- [ ] Docker Compose sobe todo o stack.

## 8. Rubrica de Auto-Avaliação

| Critério | ⭐ Básico | ⭐⭐ Intermediário | ⭐⭐⭐ Avançado |
|----------|----------|-------------------|---------------|
| Instrumentação | 2 métricas | 4 métricas com labels | 5+ métricas + histograma |
| Dashboard | 3 painéis | 6 painéis infra + modelo | 8+ painéis + template variables |
| Alertas | Sem alerta | 1 alerta threshold | 2+ alertas multi-condition |

## 9. Matriz de Rastreabilidade

| Objetivo | Requisito | Etapa | Entregável | Aulas |
|----------|-----------|-------|------------|-------|
| O1 | RF-01 | 2 | E1 | Aula 02 |
| O2 | RF-02 | 3 | E2 | Aula 03 |
| O3 | RF-03 | 4 | E2 | Aula 03 |
| O4 | — | 1 | E3 | Aula 01 |

## 10. Extensões Opcionais

- Adicionar Prometheus no Kubernetes com ServiceMonitor (Aula 04).
- Integrar Azure Monitor ou CloudWatch como data source adicional (Aulas 05–06).
- Experimentar OpenTelemetry para traces distribuídos (Aula 08).

## 11. Checklist Rápido

- [ ] Li as aulas 01–08.
- [ ] Elaborei plano de observabilidade.
- [ ] Instrumentei API com Prometheus client.
- [ ] Criei dashboard Grafana ≥ 6 painéis.
- [ ] Configurei alerta.
- [ ] Documento ≤ 2 páginas.
