# 📖 Grupo de Estudos 1 — Detecção de Data Drift e Monitoramento de Modelo

> **Fase:** 04 — Monitoramento e Governança | **Etapa do TC:** 1

---

## 📋 Foco da Sessão

Detecção automatizada de drift feature a feature e monitoramento proativo de degradação do modelo.

**Disciplinas de referência:**
- [`01-data-drift`](../../01-data-drift/)
- [`02-ferramentas-monitoramento-modelos`](../../02-ferramentas-monitoramento-modelos/)

---

## 🎯 Objetivos

- Treinar MLP PyTorch Lightning para scoring de crédito
- Implementar detecção de drift feature a feature (KS, PSI, Qui-quadrado)
- Aplicar ≥ 1 métrica avançada (JS Divergence, Wasserstein ou MMD)
- Classificar features por nível de drift (Estável / Moderado / Significativo)
- Gerar relatório de drift automatizado
- Definir plano de 5 categorias de métricas

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- O que é data drift e por que modelos degradam em produção?
- Tipos de drift: covariada, prior probability, concept drift
- Métricas de drift: KS test, PSI, Qui-quadrado — quando usar cada uma?
- Categorias de monitoramento: performance, dados, predições, operacional, negócio

### 2. Exercício Guiado (~40 min)

1. **MLP para crédito:**
   - Dataset de crédito (German Credit ou similar)
   - MLP com PyTorch Lightning + MLflow tracking
   - Baseline com LogisticRegression

2. **Detecção de drift:**
   ```python
   from scipy.stats import ks_2samp, chi2_contingency

   # Para features numéricas
   stat, pvalue = ks_2samp(reference_data[feature], production_data[feature])

   # PSI (Population Stability Index)
   def calculate_psi(reference, production, bins=10):
       # ... implementar
   ```
   - Aplicar para ≥ 5 features
   - Classificar: PSI < 0.1 (Estável), 0.1-0.25 (Moderado), > 0.25 (Significativo)

3. **Métrica avançada:**
   - Implementar JS Divergence ou Wasserstein distance
   - Comparar sensibilidade com KS e PSI

4. **Relatório automatizado:**
   - Tabela: feature | métrica | valor | classificação
   - Gráficos de distribuição: referência (azul) vs. produção (vermelho)
   - Salvar como HTML ou PDF

### 3. Discussão Aberta (~20 min)

- Drift detectado: re-treinar imediatamente ou investigar primeiro?
- Como definir thresholds de drift para um modelo de crédito (regulado)?
- Diferença entre drift nos dados vs. drift no modelo: como distinguir?
- Frequência de monitoramento: real-time vs. batch diário?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 1:**

- [ ] MLP treinada e registrada no MLflow Model Registry
- [ ] Drift detection para ≥ 5 features com classificação
- [ ] ≥ 1 métrica avançada implementada (JS, Wasserstein ou MMD)
- [ ] Relatório de drift gerado automaticamente
- [ ] Plano de 5 categorias de métricas documentado

---

## 📚 Referências

- Material das disciplinas: [`01-data-drift`](../../01-data-drift/), [`02-ferramentas-monitoramento-modelos`](../../02-ferramentas-monitoramento-modelos/)
- [Evidently AI — Data Drift](https://docs.evidentlyai.com/)
- [NannyML — Performance Estimation](https://nannyml.readthedocs.io/)
- [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/)
