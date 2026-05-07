# 📖 Grupo de Estudos 1 — Deploy em Nuvem e Escolha Arquitetural

> **Fase:** 03 — Cloud e MLOps | **Etapa do TC:** 1

---

## 📋 Foco da Sessão

Decisão de arquitetura de deploy e setup da infraestrutura para servir modelo de triagem médica.

**Disciplina de referência:**
- [`01-deploy-em-nuvem`](../../01-deploy-em-nuvem/)

---

## 🎯 Objetivos

- Analisar paradigmas de deploy (batch, real-time, serverless) e justificar escolha
- Documentar decisão arquitetural com framework de decisão
- Servir modelo via FastAPI em container Docker (deploy inicial)
- Medir baseline de latência e throughput
- Estimar custos (FinOps) da solução escolhida

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Paradigmas de deploy: batch vs. real-time vs. serverless
- Quando usar cada um? Trade-offs de custo, latência, complexidade
- Framework de decisão arquitetural: como documentar ADRs (Architecture Decision Records)
- FinOps básico: quanto custa servir N requisições/dia?

### 2. Exercício Guiado (~40 min)

1. **Análise de paradigma:**
   - Para triagem médica: por que real-time é a escolha mais provável?
   - Documentar em formato ADR: contexto, decisão, consequências
2. **Deploy inicial:**
   - FastAPI com endpoint `/predict` que recebe texto de laudo
   - Container Docker servindo o modelo
   - Testar localmente com `curl` ou `httpie`
3. **Baseline de performance:**
   - Medir latência P50, P95, P99 com `wrk` ou `locust`
   - Medir throughput (requests/segundo)
   - Identificar gargalos: tokenização? inferência? IO?
4. **Estimativa de custo:**
   - Volume esperado: X laudos/dia
   - CPU vs. GPU: custo/benefício para DistilBERT
   - Cloud options: Container Apps, ECS, Cloud Run

### 3. Discussão Aberta (~20 min)

- SLO de P95 < 200 ms: é viável com DistilBERT em CPU?
- Quando migrar de CPU para GPU? Análise de break-even
- Serverless (Lambda/Functions) para NLP: limitações de cold start
- Como justificar custos para stakeholders não-técnicos?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 1:** API funcional em container + documento de decisão arquitetural

- [ ] ADR documentando paradigma escolhido
- [ ] API FastAPI servindo modelo em Docker
- [ ] Baseline de latência (P50, P95, P99)
- [ ] Estimativa de custo FinOps
- [ ] Gargalos identificados para otimização futura

---

## 📚 Referências

- Material da disciplina: [`01-deploy-em-nuvem`](../../01-deploy-em-nuvem/)
- [Architecture Decision Records](https://adr.github.io/)
- [Locust Load Testing](https://locust.io/)
- [Azure Container Apps Pricing](https://azure.microsoft.com/pricing/details/container-apps/)
