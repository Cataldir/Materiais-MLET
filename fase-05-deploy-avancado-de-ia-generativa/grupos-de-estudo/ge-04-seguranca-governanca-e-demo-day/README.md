# 📖 Grupo de Estudos 4 — Segurança, Governança e Demo Day

> **Fase:** 05 — Deploy Avançado de IA Generativa | **Etapa do TC:** 4
> **Integra:** Fase 04 (LGPD, fairness, explicabilidade) + Fase 05 (guardrails, OWASP, conformidade)

---

## 📋 Foco da Sessão

Guardrails de segurança, conformidade LGPD para LLMs, preparação para o Demo Day com empresa.

**Disciplinas de referência:**
- [`05-seguranca-guardrails-conformidade`](../../05-seguranca-guardrails-conformidade/)
- Competências de Fase 04: governança, compliance

---

## 🎯 Objetivos

- Implementar guardrails de entrada e saída (topic blocking, PII detection, toxicity)
- Mapear OWASP Top 10 para LLMs no contexto do projeto
- Criar plano de conformidade LGPD para sistema generativo
- Gerar System Card documentando riscos e mitigações
- Preparar pitch para Demo Day (≤ 10 min + 5 min Q&A)
- Consolidar repositório final

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Guardrails: por que LLMs precisam de "grades de proteção"?
- OWASP Top 10 para LLMs: prompt injection, data leakage, insecure output handling
- PII detection: Presidio, regex, NER — abordagens complementares
- System Card vs. Model Card: diferença para sistemas compostos
- Demo Day: como fazer pitch técnico para banca empresa + academia

### 2. Exercício Guiado (~40 min)

1. **Guardrails de entrada:**
   ```python
   # Topic blocking
   blocked_topics = ["concorrentes", "dados internos", "opiniões pessoais"]

   # PII detection com Presidio
   from presidio_analyzer import AnalyzerEngine
   analyzer = AnalyzerEngine()
   results = analyzer.analyze(text=user_input, language="pt")
   ```
   - Bloquear prompts com tópicos proibidos
   - Detectar e mascarar PII antes de enviar ao LLM

2. **Guardrails de saída:**
   - Verificar: output não contém PII
   - Verificar: output não é tóxico (toxicity classifier)
   - Verificar: output está no domínio esperado (relevancy check)
   - Fallback: resposta padrão se guardrail triggered

3. **OWASP Top 10 para LLMs:**
   - Mapear ≥ 5 riscos relevantes ao projeto
   - Para cada: descrição, impacto, mitigação implementada
   - Documentar no System Card

4. **Conformidade LGPD:**
   - Dados de prompt: são dados pessoais? Base legal?
   - Logging de conversas: retenção, acesso, exclusão
   - Direitos do titular: como implementar "right to be forgotten" em RAG?
   - DPIA para o sistema generativo

5. **Preparação Demo Day:**
   - Pitch structure (10 min):
     - Problema da empresa (2 min)
     - Abordagem técnica (3 min)
     - Demonstração ao vivo (3 min)
     - Resultados e próximos passos (2 min)
   - Antecipar perguntas da empresa e da banca
   - Praticar timing

### 3. Discussão Aberta (~20 min)

- Guardrails: quanto "seguro" é seguro o suficiente?
- Prompt injection: é possível prevenir completamente?
- LGPD para LLMs: área cinzenta — como navegar?
- Demo Day: como comunicar incerteza sem perder credibilidade?
- Repositório final: checklist de completude

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 4:**

- [ ] Guardrails de entrada implementados (topic blocking + PII)
- [ ] Guardrails de saída implementados (toxicity + relevancy)
- [ ] OWASP Top 10 mapeado (≥ 5 riscos)
- [ ] Plano de conformidade LGPD documentado
- [ ] System Card completo
- [ ] Pitch estruturado e praticado (≤ 10 min)
- [ ] Repositório final consolidado
- [ ] *(Opcional)* Deploy em nuvem com endpoint público

---

## 📚 Referências

- Material da disciplina: [`05-seguranca-guardrails-conformidade`](../../05-seguranca-guardrails-conformidade/)
- [OWASP Top 10 for LLM Applications](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [Microsoft Presidio — PII Detection](https://microsoft.github.io/presidio/)
- [NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)
- Competências de Fase 04: LGPD, fairness, explicabilidade

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
