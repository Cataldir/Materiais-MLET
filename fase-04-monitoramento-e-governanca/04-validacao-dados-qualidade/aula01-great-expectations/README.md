# Aula 01 - Great Expectations com especificacoes locais

Pacote canonico leve para introduzir suites de expectativa e checkpoints sem exigir instalacao obrigatoria do Great Expectations. O script usa um Adapter opcional para detectar a biblioteca e, na ausencia dela, executa uma versao local baseada em especificacoes declarativas.

## Objetivo didatico

- mostrar o formato mental de expectativas declarativas para qualidade de dados;
- separar a definicao das regras da execucao do checkpoint;
- manter um contrato testavel que funcione em qualquer ambiente local.

## O que foi preservado

- especificacoes declarativas para regras de faixa, completude e cardinalidade;
- Adapter para caminho opcional com Great Expectations;
- avaliacao estilo checkpoint sobre datasets valido e invalido.

## O que foi simplificado

- sem contexto de projeto GX ou datasource persistido;
- sem dependencia obrigatoria da biblioteca;
- foco em algumas expectativas de alto valor didatico.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula01-great-expectations
python ge_validation.py
```

## Arquivos

- `ge_validation.py`: especificacoes locais, datasets sinteticos e checkpoint enxuto.

## Observacoes didaticas

- o material destaca o conceito de expectation suite antes da ferramenta em si;
- a mesma declaracao pode ser expandida para pipelines maiores com uma biblioteca completa;
- o fallback local facilita smoke tests e ambientes de estudo mais leves.