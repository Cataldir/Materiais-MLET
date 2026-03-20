# 06 — Inferência Causal e Monitoramento Prescritivo

> 6h de vídeo · 6 aulas

## Por que esta disciplina importa

Monitorar correlação é útil; entender causa e efeito é o passo que permite intervir com mais confiança. Esta disciplina introduz raciocínio causal como evolução da observabilidade tradicional, aproximando diagnóstico, experimento e decisão prescritiva em sistemas de ML.

## O que você deve aprender

- interpretar DAGs, SCMs e noções fundamentais de causalidade;
- estimar efeitos causais com bibliotecas como DoWhy e EconML;
- aplicar uplift modeling e análise causal em decisões de intervenção;
- conectar A/B testing, monitoramento e prescrição de ações;
- consolidar um projeto que vá além de descrição e predição.

## Como usar este material

1. Comece pelos fundamentos conceituais, porque a disciplina exige mudança de mentalidade.
2. Em seguida, use os exemplos com bibliotecas para concretizar os conceitos.
3. Trate uplift e A/B testing como aplicações práticas do raciocínio causal.
4. Feche com monitoramento prescritivo e projeto completo para integrar teoria e uso operacional.

## Como referenciar esta disciplina no repositório

- O índice da disciplina está em `fase-04-monitoramento-e-governanca/06-inferencia-causal/`.
- Ao discutir técnica ou biblioteca específica, cite a aula correspondente para manter o contexto correto.
- O README oferece o enquadramento da trilha; scripts e notebooks são a evidência executável de cada abordagem.
- A camada de governança do curso permanece como referência oficial para processos e avaliação.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Do ponto de vista executivo, causalidade melhora priorização de intervenção e evita decisões guiadas apenas por correlação espúria. Academicamente, a disciplina amplia o repertório metodológico do estudante, conectando estatística, experimentação e tomada de decisão baseada em efeito estimado.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-dags-scm/) | DAGs, SCMs, do-calculus | `causal_dags.py` |
| [02](aula02-dowhy-econml/) | DoWhy + EconML: estimacao de efeito causal | `causal_effect_estimation.py`, notebook |
| [03](aula03-uplift-modeling/) | Uplift Modeling com CausalML/EconML | `uplift_model.py` |
| [04](aula04-ab-testing/) | A/B Testing com análise causal | `ab_testing.py` |
| [05](aula05-monitoramento-prescritivo/) | Monitoramento prescritivo | `prescriptive_monitoring.py` |
| [06](aula06-projeto-completo/) | Projeto completo | notebook integrador |
