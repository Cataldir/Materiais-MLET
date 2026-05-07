# 📖 Grupo de Estudos 4 — Governança, Compliance e Inferência Causal

> **Fase:** 04 — Monitoramento e Governança | **Etapa do TC:** 4

---

## 📋 Foco da Sessão

LGPD/GDPR compliance, explicabilidade, fairness audit e inferência causal aplicada.

**Disciplinas de referência:**
- [`05-governanca-compliance`](../../05-governanca-compliance/)
- [`06-inferencia-causal`](../../06-inferencia-causal/)

---

## 🎯 Objetivos

- Mapear fluxo de dados com bases legais (LGPD) por etapa do pipeline
- Implementar anonimização (k-anonymity ou pseudonimização)
- Gerar explicações com SHAP (global + local)
- Conduzir fairness audit com ≥ 1 métrica por grupo protegido
- Criar Model Card (template Mitchell et al.) e DPIA simplificada
- Construir DAG causal com DoWhy e estimar ATE + CATE

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- LGPD: bases legais, direitos do titular, DPIA
- Explicabilidade: SHAP (Shapley values) — interpretação global vs. local
- Fairness: disparate impact, equalized odds, demographic parity
- Inferência causal: diferença entre correlação e causalidade
- DoWhy: framework para causal inference (identificação → estimação → refutação)

### 2. Exercício Guiado (~40 min)

1. **Mapeamento LGPD:**
   - Listar dados pessoais no dataset de crédito
   - Definir base legal para cada uso (consentimento, execução contratual, interesse legítimo)
   - Identificar: quem acessa, por quanto tempo, onde armazena

2. **Anonimização:**
   - k-anonymity: generalizar idade em faixas, CEP em região
   - Ou pseudonimização: hash de CPF/nome com salt

3. **SHAP:**
   ```python
   import shap
   explainer = shap.Explainer(model, X_train)
   shap_values = explainer(X_test)
   shap.summary_plot(shap_values)  # global
   shap.waterfall_plot(shap_values[0])  # local
   ```

4. **Fairness audit:**
   ```python
   from fairlearn.metrics import MetricFrame, selection_rate
   metric_frame = MetricFrame(
       metrics=selection_rate,
       y_true=y_test, y_pred=predictions,
       sensitive_features=df_test['gender']
   )
   ```
   - Calcular disparate impact ratio
   - Documentar: grupo prejudicado, magnitude, mitigação proposta

5. **Inferência causal (DoWhy):**
   - Definir DAG: treatment (ex.: limite de crédito), outcome (default)
   - Identificar: backdoor criterion
   - Estimar ATE com DoWhy + CATE com EconML (CausalForestDML)
   - Refutação: placebo treatment, random common cause

### 3. Discussão Aberta (~20 min)

- LGPD para modelos de crédito: quais os riscos reais de não-compliance?
- SHAP: quando o modelo não é explicável o suficiente para reguladores?
- Fairness vs. performance: é possível ter os dois? Trade-offs reais
- Inferência causal: como convencer stakeholders de que "correlação ≠ causalidade"?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 4:**

- [ ] Mapeamento de fluxo de dados com bases legais LGPD
- [ ] Anonimização aplicada (k-anonymity ou pseudonimização)
- [ ] SHAP: summary plot (global) + waterfall (local)
- [ ] Fairness audit com ≥ 1 métrica por grupo protegido
- [ ] Model Card completa (template Mitchell et al.)
- [ ] DPIA simplificada documentada
- [ ] DAG causal com DoWhy + ATE estimado
- [ ] ≥ 2 refutation checks passando
- [ ] Vídeo STAR ≤ 5 min

---

## 📚 Referências

- Material das disciplinas: [`05-governanca-compliance`](../../05-governanca-compliance/), [`06-inferencia-causal`](../../06-inferencia-causal/)
- [SHAP Documentation](https://shap.readthedocs.io/)
- [Fairlearn](https://fairlearn.org/)
- [DoWhy — Causal Inference](https://www.pywhy.org/dowhy/)
- [EconML](https://econml.azurewebsites.net/)
- [LGPD — Lei 13.709/2018](http://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
