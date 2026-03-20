# Aula 02 - Avaliacao automatizada para respostas generativas

Pacote canonico leve para demonstrar avaliacao automatizada de respostas generativas com heuristicas locais que se comportam como um juiz simples. O objetivo e discutir grounding, cobertura e risco de alucinacao sem depender de chamadas externas a modelos.

## Objetivo didatico

- comparar respostas bem fundamentadas com respostas superficiais ou alucinadas;
- introduzir a ideia de um avaliador automatizado antes de ferramentas mais completas;
- ligar qualidade de resposta a criterios observaveis e repetiveis.

## O que foi preservado

- comparacao entre resposta boa, incompleta e alucinada;
- dimensoes de cobertura e grounding ao contexto;
- resumo final pronto para conversa executiva sobre qualidade operacional.

## O que foi simplificado

- sem uso de APIs de judge model ou bibliotecas externas de avaliacao;
- sem embeddings ou retrieval real como dependencia de execucao;
- heuristicas lexicais pequenas para favorecer debug e reproducao local.

## Execucao

```bash
cd fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/aula02-avaliacao-automatizada
python ragas_evaluation.py
```

## Arquivos

- `ragas_evaluation.py`: compara respostas sinteticas usando cobertura, grounding e decisao final.
- `02_avaliacao_automatizada_local.ipynb`: notebook local com a mesma avaliacao.

## Observacoes didaticas

- a aula nao tenta reproduzir RAGAS fielmente; ela constrói intuicao de avaliacao automatizada com sinal observavel;
- respostas com boa cobertura, mas sem grounding, continuam inadequadas para producao.