# 📖 Grupo de Estudos 2 — Modelo Avançado e Agente com LLM

> **Fase:** 05 — Deploy Avançado de IA Generativa | **Etapa do TC:** 2
> **Integra:** Fase 03 (API, CI/CD) + Fase 05 (LLM serving, agente ReAct, RAG)

---

## 📋 Foco da Sessão

Serving de LLM otimizado, construção de agente ReAct e pipeline RAG sobre dados da empresa.

**Disciplinas de referência:**
- [`01-deploy-modelos-ia-generativa`](../../01-deploy-modelos-ia-generativa/)
- [`02-deploy-agentes-llms`](../../02-deploy-agentes-llms/)

---

## 🎯 Objetivos

- Servir LLM open-source otimizado (vLLM ou BentoML)
- Aplicar quantização (GPTQ/AWQ/int8) para reduzir VRAM
- Implementar agente ReAct com ≥ 3 tools integradas ao domínio
- Construir RAG pipeline: embedding → chunking → vector store → retrieval → geração
- API de inferência com endpoint documentado
- CI/CD pipeline funcional
- Benchmark de performance (latência, throughput, VRAM)

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- LLM serving: vLLM (continuous batching, PagedAttention) vs. BentoML
- Quantização: GPTQ, AWQ, bitsandbytes — trade-offs de qualidade vs. velocidade
- Agentes ReAct: raciocínio + ação iterativos
- RAG: por que "context > fine-tuning" para dados específicos da empresa

### 2. Exercício Guiado (~40 min)

1. **Serving de LLM:**
   - Escolher modelo open-source (Llama 3, Mistral, Phi-3)
   - Deploy com vLLM ou BentoML
   - Aplicar quantização INT8 ou GPTQ
   - Medir: latência, tokens/segundo, VRAM usage

2. **Agente ReAct:**
   ```python
   from langchain.agents import create_react_agent

   tools = [
       search_company_docs,   # RAG over company data
       query_database,        # SQL queries
       calculate_metrics,     # Business KPI calculator
   ]
   agent = create_react_agent(llm, tools, prompt)
   ```
   - ≥ 3 tools relevantes ao domínio da empresa

3. **RAG pipeline:**
   - Chunking de documentos da empresa (overlap, semantic chunking)
   - Embedding com modelo open-source (e5, bge)
   - Vector store: FAISS ou ChromaDB
   - Retrieval: top-k + reranking
   - Generation: LLM gera resposta com contexto

4. **CI/CD + API:**
   - FastAPI ou BentoML endpoint documentado
   - GitHub Actions: lint → test → build → deploy (staging)
   - Testes: smoke test de geração, latência < threshold

### 3. Discussão Aberta (~20 min)

- vLLM vs. BentoML: quando usar cada um?
- Quantização: quanto de qualidade perdemos na prática?
- Agentes com tools: como evitar loops infinitos?
- RAG: quando retrieval falha (low recall)?
- GPU costs: como justificar para a empresa?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 2:**

- [ ] LLM servido via API com quantização aplicada
- [ ] Agente ReAct funcional com ≥ 3 tools relevantes ao domínio
- [ ] RAG retornando contexto relevante dos dados da empresa
- [ ] CI/CD pipeline funcional
- [ ] Benchmark documentado com ≥ 3 configurações

---

## 📚 Referências

- Material das disciplinas: [`01-deploy-modelos-ia-generativa`](../../01-deploy-modelos-ia-generativa/), [`02-deploy-agentes-llms`](../../02-deploy-agentes-llms/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [LangChain Agents](https://python.langchain.com/docs/modules/agents/)
- [ChromaDB](https://docs.trychroma.com/)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
