# Aula 03 - Pydantic para validacao em runtime

Pacote canonico leve para validar payloads de inferencia em runtime com uma cadeia de validadores locais e um Strategy opcional usando Pydantic quando disponivel. O foco da aula e mostrar como proteger fronteiras de sistema sem acoplar a logica de negocio ao mecanismo de validacao.

## Objetivo didatico

- validar campos obrigatorios, faixas e tipos antes de processar a inferencia;
- separar schema validation de regras de negocio adicionais;
- demonstrar Chain of Responsibility para compor validadores pequenos.

## O que foi preservado

- `pydantic` como caminho opcional para schema validation;
- cadeia de validadores locais para checks de negocio e integridade;
- exemplos validos e invalidos para smoke tests e walkthrough local.

## O que foi simplificado

- sem API web ou middleware de framework;
- sem dependencia obrigatoria de Pydantic;
- foco em payload tabular pequeno e regras deterministicas.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula03-pydantic-runtime
python pydantic_validation.py
```

## Arquivos

- `pydantic_validation.py`: strategy opcional com Pydantic e cadeia de validadores locais.

## Observacoes didaticas

- a cadeia facilita adicionar novos checks sem inflar uma unica funcao;
- Pydantic cobre schema e coercao, mas regras de negocio continuam explicitas na pipeline;
- o mesmo padrao serve para APIs, jobs de scoring e workers assincros.