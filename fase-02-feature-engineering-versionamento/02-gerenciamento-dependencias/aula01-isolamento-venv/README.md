# Aula 01 - Isolamento com venv e virtualenv

Pack local para discutir isolamento de ambiente sem depender de criacao real de ambientes durante a leitura. A aula usa um factory para gerar blueprints de setup e ativacao para diferentes gerenciadores, preservando comportamento determinista e seguro.

## Objetivo didatico

- mostrar por que isolamento e um contrato operacional minimo;
- comparar `venv` e `virtualenv` de forma concreta e local;
- padronizar comandos de criacao, ativacao e instalacao para projetos de ML.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/aula01-isolamento-venv
python venv_factory.py
```

## Arquivos

- `venv_factory.py`: gera blueprints deterministas para isolamento local.

## Observacoes didaticas

- a aula evita criar ambientes reais para nao introduzir efeitos colaterais;
- o importante aqui e padronizar especificacao e onboarding do projeto;
- os comandos emitidos podem ser copiados para um projeto real quando necessario.