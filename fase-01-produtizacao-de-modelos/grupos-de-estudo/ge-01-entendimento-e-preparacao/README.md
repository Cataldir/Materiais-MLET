# 📖 Grupo de Estudos 1 — Entendimento e Preparação

> **Fase:** 01 — Produtização de Modelos | **Etapa do TC:** 1

---

## 📋 Foco da Sessão

Formulação do problema de negócio, exploração de dados e construção de baselines para previsão de churn.

**Disciplinas de referência:**
- [`01-ciclo-de-vida-de-modelos`](../../01-ciclo-de-vida-de-modelos/)
- [`02-fundamentos-modelos-ml`](../../02-fundamentos-modelos-ml/)

---

## 🎯 Objetivos

- Entender o problema de churn como caso de classificação binária
- Preencher o ML Canvas (stakeholders, métricas de negócio, SLOs)
- Realizar EDA completa: volume, qualidade, distribuição, data readiness
- Definir métricas técnicas (AUC-ROC, PR-AUC, F1) e de negócio (custo de churn evitado)
- Treinar baselines com DummyClassifier e Regressão Logística
- Registrar experimentos no MLflow

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- O que é o ciclo de vida de modelos de ML?
- Como formular um problema de classificação a partir de uma necessidade de negócio?
- O que é o ML Canvas e quais seus componentes?
- Diferença entre métrica técnica e métrica de negócio

### 2. Exercício Guiado (~40 min)

1. **ML Canvas do Tech Challenge:** preencher em grupo o canvas para o problema de churn
   - Stakeholders: quem usa o modelo, quem é impactado
   - Dados: quais features estão disponíveis no dataset Telco
   - Métricas: definir threshold de AUC-ROC mínimo e custo de FP vs FN
2. **EDA rápida:** carregar o dataset, verificar tipos, missing values, distribuição do target
3. **Baseline:** treinar DummyClassifier + LogisticRegression, logar no MLflow

### 3. Discussão Aberta (~20 min)

- Quais features parecem mais preditivas? Como decidir?
- Qual a proporção de churn no dataset? Precisamos de balanceamento?
- Como o MLflow ajuda na comparabilidade entre experimentos?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 1:** Notebook de EDA + baselines registrados no MLflow

- [ ] ML Canvas preenchido
- [ ] EDA com análise de distribuição e qualidade
- [ ] Métricas técnicas e de negócio definidas
- [ ] Baseline DummyClassifier + LogReg treinados
- [ ] Experimentos registrados no MLflow

---

## 📚 Referências

- Material da disciplina: [`01-ciclo-de-vida-de-modelos`](../../01-ciclo-de-vida-de-modelos/)
- Dataset sugerido: [Telco Customer Churn — IBM](https://www.kaggle.com/datasets/blastchar/telco-customer-churn)
- [MLflow Quickstart](https://mlflow.org/docs/latest/quickstart.html)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
