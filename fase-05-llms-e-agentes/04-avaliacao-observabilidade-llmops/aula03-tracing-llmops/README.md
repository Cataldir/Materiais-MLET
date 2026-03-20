# Aula 03 - Tracing local para fluxos de LLMOps

Pacote canonico leve para tornar um fluxo generativo observavel sem exigir LangSmith ou Phoenix como caminho default. A aula mostra como representar retrieval, prompt, geracao e avaliacao em um trace unico e como derivar custo, latencia e risco operacional dessa sequencia.

## Objetivo didatico

- descrever um fluxo de RAG em etapas observaveis;
- agregar tokens, latencia e custo estimado em um resumo unico;
- sinalizar riscos quando o trace indica grounding fraco ou custo excessivo.

## O que foi preservado

- decomposicao de retrieval, prompt building, generation e evaluation;
- metricas de latencia, tokens e custo estimado;
- leitura operacional de risco a partir do trace.

## O que foi simplificado

- sem backend SaaS de tracing como requisito;
- sem chamadas reais a LLM ou vector store;
- dados e tokens sinteticos para manter execucao local e deterministica.

## Execucao

```bash
cd fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula03-tracing-llmops
python llm_tracing.py
```

## Arquivos

- `llm_tracing.py`: monta um trace local de LLMOps, calcula metricas e sinaliza riscos.
- `03_tracing_llmops_local.ipynb`: notebook local com o mesmo fluxo do script.

## Observacoes didaticas

- a aula ensina o contrato de tracing antes da ferramenta de mercado;
- risco de grounding fraco aparece como propriedade do trace, nao como opiniao isolada.