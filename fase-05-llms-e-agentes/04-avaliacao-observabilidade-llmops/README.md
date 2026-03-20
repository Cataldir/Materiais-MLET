# 04 — Avaliação e Observabilidade em LLMOps

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

LLMs geram saídas probabilísticas, caras e difíceis de inspecionar sem instrumentação adequada. Esta disciplina mostra como medir qualidade, rastrear execução e controlar custo e latência em aplicações generativas, tornando LLMOps um processo verificável em vez de intuitivo.

## O que você deve aprender

- aplicar métricas clássicas e modernas de avaliação em NLP e geração;
- usar abordagens automatizadas como RAGAS e LLM-as-judge com senso crítico;
- instrumentar tracing e observabilidade para fluxos generativos;
- acompanhar custo e latência como dimensões de qualidade operacional;
- consolidar uma visão de LLMOps ponta a ponta.

## Como usar este material

1. Comece pelas métricas para construir vocabulário de avaliação.
2. Em seguida, compare métodos automatizados e seus limites.
3. Use tracing, custo e latência para fechar a dimensão operacional.
4. Trate o projeto final como síntese do que significa operar LLMs com evidência.

## Como referenciar esta disciplina no repositório

- O caminho principal é `fase-05-llms-e-agentes/04-avaliacao-observabilidade-llmops/`.
- Ao citar uma técnica de avaliação ou tracing, referencie a aula correspondente.
- O README organiza a interpretação da trilha; scripts e notebooks mostram como a medição é implementada.
- Critérios institucionais de avaliação do curso permanecem na governança principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, esta disciplina ajuda a tomar decisões melhores sobre qualidade percebida, custo e confiabilidade de aplicações generativas. Academicamente, ela oferece uma base concreta para discutir avaliação de sistemas probabilísticos, instrumentação e validade de proxies automáticos de qualidade.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-metricas-nlp/) | Métricas: BLEU, ROUGE, BERTScore | `nlp_metrics.py` |
| [02](aula02-avaliacao-automatizada/) | RAGAS, LLM-as-judge | `ragas_evaluation.py` |
| [03](aula03-tracing-llmops/) | Tracing: LangSmith, Phoenix/Arize | `llm_tracing.py` |
| [04](aula04-custo-latencia/) | Custo e latência: tracking e otimização | `cost_tracker.py` |
| [05](aula05-projeto-llmops/) | Projeto LLMOps end-to-end | notebook integrador |
