# 📖 Grupo de Estudos 3 — Monitoramento e Observabilidade

> **Fase:** 03 — Cloud e MLOps | **Etapa do TC:** 3

---

## 📋 Foco da Sessão

Stack de observabilidade completo para modelo em produção: Prometheus + Grafana + SLOs + alertas.

**Disciplinas de referência:**
- [`04-monitoracao-performance`](../../04-monitoracao-performance/)
- [`05-servicos-de-monitoracao`](../../05-servicos-de-monitoracao/)

---

## 🎯 Objetivos

- Instrumentar API com `prometheus_client` (≥ 4 métricas customizadas)
- Criar dashboard Grafana com ≥ 6 painéis
- Definir SLOs: P95 < 200 ms, availability > 99.5%, drift PSI < 0.1
- Configurar alertas (latência, error rate, prediction skew)
- Docker Compose: API + Prometheus + Grafana

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Observabilidade: métricas, logs, traces — pilares
- Prometheus: modelo pull, PromQL básico, tipos de métricas (Counter, Histogram, Gauge)
- Grafana: dashboards, alerting, template variables
- SLOs vs. SLAs vs. SLIs: diferenças práticas

### 2. Exercício Guiado (~40 min)

1. **Instrumentação Prometheus:**
   ```python
   from prometheus_client import Counter, Histogram, Gauge

   PREDICTIONS = Counter('predictions_total', 'Total predictions', ['class'])
   LATENCY = Histogram('prediction_latency_seconds', 'Prediction latency')
   CONFIDENCE = Histogram('prediction_confidence', 'Confidence scores')
   MODEL_VERSION = Gauge('model_version_info', 'Current model version')
   ```
   - Integrar na API FastAPI como middleware

2. **Docker Compose:**
   ```yaml
   services:
     api: ...
     prometheus:
       image: prom/prometheus
       volumes: [./prometheus.yml:/etc/prometheus/prometheus.yml]
     grafana:
       image: grafana/grafana
       ports: ["3000:3000"]
   ```

3. **Dashboard Grafana:**
   - Painel 1: Latência P50, P95, P99 (Histogram)
   - Painel 2: Throughput (requests/min)
   - Painel 3: Distribuição de predições por classe
   - Painel 4: Error rate (4xx, 5xx)
   - Painel 5: CPU/Memory do container
   - Painel 6: Confidence histogram

4. **Alertas:**
   - `latency_p95 > 200ms` por 5 min → warning
   - `error_rate > 1%` por 2 min → critical
   - `prediction_skew > 0.1` → drift alert

### 3. Discussão Aberta (~20 min)

- Quais métricas realmente importam para um modelo de triagem médica?
- Como definir thresholds de alerta sem falsos positivos?
- Grafana vs. Datadog vs. New Relic: trade-offs de custo
- Como monitorar model drift com Prometheus?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 3:** Stack de monitoramento funcional + dashboard JSON export

- [ ] API instrumentada com ≥ 4 métricas Prometheus
- [ ] Docker Compose: API + Prometheus + Grafana funcionando
- [ ] Dashboard com ≥ 6 painéis
- [ ] SLOs definidos e documentados
- [ ] ≥ 2 alertas configurados
- [ ] Dashboard JSON exportado no repositório

---

## 📚 Referências

- Material das disciplinas: [`04-monitoracao-performance`](../../04-monitoracao-performance/), [`05-servicos-de-monitoracao`](../../05-servicos-de-monitoracao/)
- [Prometheus Python Client](https://github.com/prometheus/client_python)
- [Grafana Dashboards](https://grafana.com/docs/grafana/latest/dashboards/)
- [Google SRE Book — SLOs](https://sre.google/sre-book/service-level-objectives/)
