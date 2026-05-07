# Fase 04 — Monitoramento e Governança

## Tech Challenge: Monitoramento End-to-End de Rede Neural em Produção com Detecção de Drift, Observabilidade e Governança

Uma fintech opera um modelo de rede neural (MLP) que aprova microcrédito em tempo real. O modelo foi treinado há 6 meses e os indicadores de negócio mostram degradação sutil. A empresa precisa de detecção de data drift automatizada, stack de observabilidade, validação de dados na ingestão, e governança (LGPD, explicabilidade, fairness) com análise causal.

---

## Grupos de Estudo

| GE | Tema | Etapa do TC | Disciplinas |
|----|------|-------------|-------------|
| [GE 01](ge-01-deteccao-de-data-drift-e-monitoramento-de-modelo/) | Detecção de Data Drift e Monitoramento | Etapa 1 | Data Drift, Ferramentas de Monitoramento |
| [GE 02](ge-02-observabilidade-metricas-logs-e-pipeline-monitoring/) | Observabilidade e Pipeline Monitoring | Etapa 2 | Monitoramento de Modelos, Pipelines |
| [GE 03](ge-03-validacao-de-dados-e-qualidade-continua/) | Validação de Dados e Qualidade | Etapa 3 | Validação de Dados, Pipelines |
| [GE 04](ge-04-governanca-compliance-e-inferencia-causal/) | Governança, Compliance e Inferência Causal | Etapa 4 | Governança LGPD, Inferência Causal |

---

## Entrega do Tech Challenge

- **Obrigatório:** Repositório GitHub + Vídeo STAR ≤ 5 min + Model Card + DPIA simplificada
- **Bibliotecas:** PyTorch · Scikit-Learn · MLflow · PyTorch Lightning

## Critérios de Avaliação

| Critério | Peso |
|----------|------|
| Rede neural + drift detection | 20% |
| Observabilidade (Prometheus + Grafana) | 20% |
| Validação de dados (Pandera + GE) | 20% |
| Governança + Inferência Causal | 20% |
| Documentação (Model Card + DPIA) | 10% |
| Vídeo STAR | 10% |
