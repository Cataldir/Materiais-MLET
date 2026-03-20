# Aula 05 - Projeto LLMOps com replay de traces

Projeto integrador local que reexecuta traces sinteticos em um pipeline pipes-and-filters para calcular risco, qualidade e decisao operacional.

## Objetivo didatico

- conectar tracing, avaliacao e gating em um fluxo unico;
- aplicar filtros pequenos e auditaveis em sequencia;
- manter o experimento leve e reproduzivel em qualquer maquina.

## Execucao

```bash
cd fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula05-projeto-llmops
python llmops_project.py
```

## Arquivos

- `llmops_project.py`: pipeline pipes-and-filters para traces locais.
- `05_projeto_llmops_local.ipynb`: notebook fino sobre o mesmo modulo.

## Observacoes didaticas

- cada filtro faz apenas uma transformacao pequena;
- o replay permite comparar diferentes traces sob a mesma regra;
- a decisao final e explicavel porque cada etapa deixa evidencias locais.