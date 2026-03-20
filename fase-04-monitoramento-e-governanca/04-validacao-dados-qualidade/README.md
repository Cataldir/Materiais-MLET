# 04 — Validação de Dados e Bibliotecas de Qualidade

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Muitos incidentes de ML não surgem no modelo, mas na entrada errada que o sistema aceita sem contestar. Esta disciplina mostra como validar dados, contratos e qualidade operacional antes que o problema se propague para treino, serving ou monitoramento tardio.

## O que você deve aprender

- usar Great Expectations para suites e checkpoints de qualidade;
- definir schemas tipados com Pandera;
- validar payloads e estruturas em runtime com Pydantic e Cerberus;
- incorporar gates de qualidade em pipelines executáveis.

## Como usar este material

1. Comece pelas ferramentas de validação mais declarativas.
2. Compare validação tabular, tipada e runtime para entender complementaridade.
3. Use a aula de gates como síntese operacional da disciplina.
4. Reaplique esses padrões em pipelines, APIs e projetos de Tech Challenge.

## Como referenciar esta disciplina no repositório

- A trilha está em `fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/`.
- Ao citar uma biblioteca, referencie a aula correspondente e o artefato principal.
- O README orienta leitura e uso; scripts, notebooks e pipelines mostram a implementação concreta.
- Regras institucionais e critérios formais permanecem na governança canônica.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Em operações reais, validação de dados reduz custo de incidente e eleva confiança em pipelines. Academicamente, a disciplina ajuda a formalizar qualidade de entrada e consistência de artefatos, aproximando engenharia de ML de práticas mais robustas de especificação e verificação.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-great-expectations/) | Great Expectations: suites + checkpoints | `ge_validation.py` |
| [02](aula02-pandera/) | Pandera: DataFrameSchema tipada | `pandera_schemas.py`, notebook |
| [03](aula03-pydantic-runtime/) | Pydantic + Cerberus para runtime validation | `pydantic_validation.py` |
| [04](aula04-pipeline-gates/) | Pipeline com gates de qualidade | `README.md`, `quality_gates.py`, notebook |
