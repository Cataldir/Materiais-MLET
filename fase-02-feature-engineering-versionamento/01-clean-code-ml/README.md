# 01 — Clean Code para Engenharia de ML

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Feature engineering e modelagem produzem valor, mas sem legibilidade e estrutura o custo de manutenção cresce rápido demais. Esta disciplina mostra como princípios de clean code ajudam times de ML a preservar clareza, separar responsabilidades e reagir melhor a mudanças de dados, regras de negócio e requisitos operacionais.

## O que você deve aprender

- reconhecer anti-patterns comuns em código de ML;
- aplicar SRP e refatoração em funções e pipelines frágeis;
- estruturar tratamento de erros e logging resiliente;
- comparar um projeto legado com sua versão refatorada para entender ganho real de qualidade.

## Como usar este material

1. Comece comparando exemplos `before/` e `after/` para visualizar o problema.
2. Reproduza a refatoração incremental antes de partir para o projeto completo.
3. Use a aula de erros e logging para pensar em robustez, não só em estilo.
4. Reaproveite estes padrões em qualquer disciplina que exponha scripts ou pipelines maiores.

## Como referenciar esta disciplina no repositório

- O caminho principal é `fase-02-feature-engineering-versionamento/01-clean-code-ml/`.
- Para discussões específicas, cite a aula que contém o anti-pattern ou refatoração de interesse.
- Este README organiza a intenção pedagógica; os diretórios `legacy/`, `refactored/`, `before/` e `after/` mostram a evidência prática.
- Questões normativas permanecem na governança principal do programa.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática de engenharia, clean code reduz risco de regressão, acelera revisão e melhora colaboração entre perfis técnicos diferentes. No contexto acadêmico, a disciplina reforça análise crítica de qualidade de artefatos e explicita critérios para avaliar estrutura, legibilidade e manutenção em software de dados.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-principios-antipatterns/) | Princípios clean code, anti-patterns | `before/`, `after/` |
| [02](aula02-srp-refatoracao/) | Funções com SRP, refatoração | `srp_example.py` |
| [03](aula03-erros-logging/) | Tratamento de erros, logging resiliente | `resilient_pipeline.py` |
| [04](aula04-projeto-refatoracao/) | Projeto completo de refatoração | `legacy/`, `refactored/` |
