# Fase 03 — Cloud e MLOps

## Tech Challenge: Deploy de Rede Neural em Produção com Pipeline CI/CD, Monitoramento e Otimização de Latência

Um hospital de referência precisa de um sistema de triagem automática de exames de texto (laudos médicos) para classificar urgência. O modelo central é uma rede neural Transformer (DistilBERT fine-tunado) servida via API REST, com pipeline CI/CD completo (GitHub Actions), monitoramento com Prometheus + Grafana e otimizações de latência para atender SLO de P95 < 200 ms.

---

## Grupos de Estudo

| GE | Tema | Etapa do TC | Disciplinas |
|----|------|-------------|-------------|
| [GE 01](ge-01-deploy-em-nuvem-e-escolha-arquitetural/) | Deploy em Nuvem e Escolha Arquitetural | Etapa 1 | Deploy em Nuvem |
| [GE 02](ge-02-cicd-e-pipeline-automatizado/) | CI/CD e Pipeline Automatizado | Etapa 2 | Integração CI/CD, Pipeline Automático |
| [GE 03](ge-03-monitoramento-e-observabilidade/) | Monitoramento e Observabilidade | Etapa 3 | Monitoração Performance, Serviços de Monitoração |
| [GE 04](ge-04-otimizacao-de-latencia-rede-neural-e-entrega/) | Otimização de Latência e Entrega | Etapa 4 | Latência e Performance |

---

## Entrega do Tech Challenge

- **Obrigatório:** Repositório GitHub + Vídeo de 5 minutos (método STAR)
- **Opcional:** Deploy em ambiente de produção em nuvem

## Bibliotecas Requeridas

- **PyTorch** — Rede neural (DistilBERT ou MLP)
- **Scikit-Learn** — Baselines e métricas
- **MLflow** — Tracking e Model Registry
- **PyTorch Lightning** — Estrutura de treino organizada

## Critérios de Avaliação

| Critério | Peso |
|----------|------|
| Rede neural (PyTorch/Lightning) | 20% |
| CI/CD (GitHub Actions) | 15% |
| Pipeline automatizado (Airflow) | 15% |
| Monitoramento (Prometheus + Grafana) | 15% |
| Otimização de latência | 10% |
| Documentação (README + Model Card) | 10% |
| Vídeo STAR | 10% |
| Bônus: deploy em nuvem | 5% |
