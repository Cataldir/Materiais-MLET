# 📖 Grupo de Estudos 3 — Avaliação, Monitoramento e Observabilidade

> **Fase:** 05 — Deploy Avançado de IA Generativa | **Etapa do TC:** 3
> **Integra:** Fase 03 (Prometheus, Grafana) + Fase 04 (drift, observabilidade) + Fase 05 (RAGAS, LLM-as-judge)

---

## 📋 Foco da Sessão

Avaliação rigorosa de sistemas generativos com RAGAS, LLM-as-judge, telemetria e monitoramento de drift.

**Disciplinas de referência:**
- [`04-avaliacao-observabilidade-llmops`](../../04-avaliacao-observabilidade-llmops/)

---

## 🎯 Objetivos

- Construir golden set com ≥ 20 pares (query, expected_answer, contexts)
- Avaliar com RAGAS: faithfulness, answer_relevancy, context_precision, context_recall
- Implementar LLM-as-judge com ≥ 3 critérios (incluindo negócio)
- Configurar telemetria (Langfuse ou TruLens)
- Implementar detecção de drift nos dados da empresa
- Criar dashboard de observabilidade
- Executar A/B test de prompts

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Por que avaliar LLMs é diferente de avaliar modelos tradicionais?
- RAGAS: métricas para RAG (faithfulness = não alucina, relevancy = responde à pergunta)
- LLM-as-judge: quando e como usar um modelo para avaliar outro
- Telemetria para LLMs: latência por chamada, token usage, cost tracking
- A/B testing de prompts: metodologia

### 2. Exercício Guiado (~40 min)

1. **Golden set:**
   - Criar ≥ 20 pares alinhados ao domínio da empresa
   - Formato: `{"query": ..., "expected_answer": ..., "contexts": [...]}`
   - Variar: perguntas fáceis, difíceis, edge cases, adversarial

2. **Avaliação RAGAS:**
   ```python
   from ragas import evaluate
   from ragas.metrics import faithfulness, answer_relevancy, context_precision, context_recall

   result = evaluate(
       dataset=golden_set,
       metrics=[faithfulness, answer_relevancy, context_precision, context_recall]
   )
   ```
   - Analisar: quais métricas estão baixas? Por quê?

3. **LLM-as-judge:**
   - Definir ≥ 3 critérios com a rubrica:
     - Critério 1: Corretude factual (técnico)
     - Critério 2: Completude da resposta (técnico)
     - Critério 3: Adequação ao negócio (definido com empresa)
   - Implementar avaliador com prompt estruturado + escala 1-5

4. **Telemetria:**
   - Langfuse: capturar traces de cada chamada
   - Métricas: latência, tokens in/out, custo estimado, scores
   - Dashboard: visualizar performance ao longo do tempo

5. **A/B test de prompts:**
   - Variante A: system prompt atual
   - Variante B: system prompt otimizado
   - Comparar métricas RAGAS entre variantes

### 3. Discussão Aberta (~20 min)

- Golden set: quantos pares são "suficientes"?
- LLM-as-judge: quando o avaliador também erra?
- Custo de avaliação: RAGAS em 1000 exemplos — quanto custa?
- Drift em LLMs: como detectar degradação de qualidade?
- A/B testing: significância estatística com amostras pequenas?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 3:**

- [ ] Golden set com ≥ 20 pares relevantes ao domínio da empresa
- [ ] RAGAS: 4 métricas calculadas e reportadas
- [ ] LLM-as-judge com ≥ 3 critérios (incluindo critério de negócio)
- [ ] Telemetria e dashboard funcionando end-to-end
- [ ] Detecção de drift implementada e documentada
- [ ] A/B test de prompts com ≥ 2 variantes comparadas

---

## 📚 Referências

- Material da disciplina: [`04-avaliacao-observabilidade-llmops`](../../04-avaliacao-observabilidade-llmops/)
- [RAGAS Documentation](https://docs.ragas.io/)
- [Langfuse](https://langfuse.com/docs)
- [TruLens](https://www.trulens.org/)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
