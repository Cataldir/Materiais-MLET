# 📖 Grupo de Estudos 1 — Entendimento do Problema e Pipeline de Dados

> **Fase:** 05 — Deploy Avançado de IA Generativa | **Etapa do TC:** 1
> **Integra:** Fase 01 (EDA, baselines) + Fase 02 (versionamento, Docker) + Briefing da empresa

---

## 📋 Foco da Sessão

Análise do problema real fornecido pela empresa convidada, exploração de dados e construção de pipeline reprodutível.

**Disciplinas de referência:**
- [`01-deploy-modelos-ia-generativa`](../../01-deploy-modelos-ia-generativa/)
- Competências acumuladas de Fases 01 e 02

---

## 🎯 Objetivos

- Analisar dados da empresa: EDA completa com insights relevantes
- Treinar baseline preditivo (Scikit-Learn + MLP PyTorch)
- Construir pipeline reprodutível (Docker + DVC + MLflow)
- Definir métricas alinhadas ao negócio (traduzir KPIs da empresa)
- Produzir relatório de viabilidade (≤ 2 páginas)

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Como abordar um problema "do mundo real" vs. acadêmico?
- Traduzir requisitos de negócio em métricas técnicas
- Pipeline de dados: ingestão → limpeza → feature engineering → versionamento
- Relatório de viabilidade: o que incluir para stakeholders não-técnicos

### 2. Exercício Guiado (~40 min)

1. **Análise do briefing da empresa:**
   - Qual o problema? Quem é impactado?
   - Quais dados foram fornecidos? Formatos, volumes, qualidade
   - KPIs de negócio definidos pela empresa
   - Restrições: latência, privacidade, custo

2. **EDA orientada ao negócio:**
   - Não apenas descrever dados, mas gerar insights actionable
   - Quais features parecem mais relevantes para o KPI?
   - Missing values: impacto nas métricas? Estratégia de imputação?
   - Visualizações que comunicam para a empresa

3. **Pipeline reprodutível:**
   - Docker para ambiente isolado
   - DVC para versionar dados da empresa
   - MLflow para tracking desde o primeiro experimento
   - `dvc repro` funciona em qualquer máquina

4. **Baseline + métricas:**
   - Modelo simples (LogReg, XGBoost) como referência
   - Mapear KPI da empresa → métrica técnica (ex.: "reduzir análise em 40%" → recall mínimo)
   - Documentar: baseline atinge ou não os critérios da empresa?

### 3. Discussão Aberta (~20 min)

- Como lidar com dados "sujos" fornecidos pela empresa?
- NDA e dados sensíveis: cuidados com versionamento
- Quando os critérios da empresa são impossíveis: como comunicar?
- Estratégia de divisão de trabalho no grupo para as 4 etapas

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 1:**

- [ ] EDA documentada com insights relevantes para o problema da empresa
- [ ] Baseline treinado e métricas reportadas (comparadas com KPIs da empresa)
- [ ] Pipeline versionado (DVC + Docker) e reprodutível
- [ ] Métricas de negócio mapeadas para métricas técnicas
- [ ] Relatório de viabilidade (≤ 2 páginas)

---

## 📚 Referências

- Material da disciplina: [`01-deploy-modelos-ia-generativa`](../../01-deploy-modelos-ia-generativa/)
- Competências de Fase 01: EDA, ML Canvas, baselines, MLflow
- Competências de Fase 02: Docker, DVC, Poetry, clean code
