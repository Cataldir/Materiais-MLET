# 📖 Grupo de Estudos 2 — Observabilidade: Métricas, Logs e Pipeline Monitoring

> **Fase:** 04 — Monitoramento e Governança | **Etapa do TC:** 2

---

## 📋 Foco da Sessão

Stack de observabilidade com Prometheus + Grafana, logging estruturado e monitoramento de pipelines.

**Disciplinas de referência:**
- [`02-ferramentas-monitoramento-modelos`](../../02-ferramentas-monitoramento-modelos/)
- [`03-monitoramento-pipelines`](../../03-monitoramento-pipelines-infra/)

---

## 🎯 Objetivos

- Instrumentar API de inferência com Prometheus (≥ 5 métricas)
- Criar dashboard Grafana com ≥ 6 painéis e template variables
- Implementar logging estruturado (JSON) com campos padronizados
- Configurar alertas multi-condition
- Docker Compose do stack completo
- Monitoramento de pipeline de treino com callbacks e runbooks

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Pilares de observabilidade: métricas, logs, traces
- Prometheus: pull model, histograms vs. summaries
- Logging estruturado vs. `print()`: por que JSON?
- Runbooks: documentação operacional para cenários de falha

### 2. Exercício Guiado (~40 min)

1. **Instrumentação Prometheus:**
   - `predictions_total` (Counter): por classe e model_version
   - `prediction_latency_seconds` (Histogram): com buckets
   - `prediction_confidence` (Histogram): distribuição de confiança
   - `error_total` (Counter): por tipo de erro
   - `model_info` (Gauge): versão, timestamp de treino

2. **Dashboard Grafana:**
   - Template variables: `$model_version`, `$environment`
   - Painel 1: Latência P50/P95/P99
   - Painel 2: Throughput (req/min)
   - Painel 3: Distribuição de predições
   - Painel 4: Error rate
   - Painel 5: Confidence histogram
   - Painel 6: Alertas ativos

3. **Logging estruturado:**
   ```python
   import structlog
   logger = structlog.get_logger()
   logger.info("prediction_made",
       request_id=req_id, model_version="v3",
       prediction="approve", confidence=0.87,
       latency_ms=45, drift_flag=False)
   ```

4. **Runbooks:**
   - Cenário 1: Fonte de dados indisponível → retry com backoff, alertar
   - Cenário 2: Schema change detectado → abortar pipeline, notificar

### 3. Discussão Aberta (~20 min)

- Log tudo ou log seletivamente? Custo de armazenamento
- Quando traces (Jaeger/Zipkin) são necessários vs. logs bastam?
- Como definir SLAs para pipeline de retreinamento?
- Runbooks: quem escreve, quem mantém atualizado?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 2:**

- [ ] Docker Compose funcional com API + Prometheus + Grafana
- [ ] ≥ 5 métricas instrumentadas com labels
- [ ] Dashboard Grafana com ≥ 6 painéis
- [ ] ≥ 2 alertas configurados
- [ ] Logging estruturado com campos padronizados
- [ ] Runbook para ≥ 2 cenários de falha

---

## 📚 Referências

- Material das disciplinas: [`02-ferramentas-monitoramento-modelos`](../../02-ferramentas-monitoramento-modelos/), [`03-monitoramento-pipelines`](../../03-monitoramento-pipelines-infra/)
- [structlog Documentation](https://www.structlog.org/)
- [Grafana Alerting](https://grafana.com/docs/grafana/latest/alerting/)
- [Google SRE — Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
