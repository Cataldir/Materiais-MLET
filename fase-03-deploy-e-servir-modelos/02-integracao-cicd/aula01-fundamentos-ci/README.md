# Aula 01 - Fundamentos de CI para ML

Pacote canonico para explicar os blocos minimos de um workflow de integracao continua orientado a projetos de ML. O material preserva o arquivo `.github/workflows/ci.yml` ja existente e adiciona um helper local e um notebook para tornar o contrato do workflow observavel sem depender da interface do GitHub.

## Objetivo didatico

- explicar o papel de lint, testes e cobertura em um fluxo de CI;
- destacar por que matriz de versoes ajuda a evitar regressao entre ambientes Python;
- oferecer um contrato local de validacao que espelha o essencial do workflow remoto.

## O que foi preservado

- workflow GitHub Actions como artefato central da aula;
- estagios de lint e testes com matriz de Python;
- validacao local com comandos equivalentes para reproducao rapida.

## O que foi simplificado

- sem secrets, ambientes de deploy ou cache avancado;
- sem parser YAML externo para manter o pack leve;
- foco em leitura do workflow e contrato local, nao em publicacao de artefatos complexos.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula01-fundamentos-ci
python ci_fundamentals.py
```

## Contrato local de validacao

```bash
ruff check .
ruff format --check .
pytest --cov --cov-report=xml -v
```

## Arquivos

- `.github/workflows/ci.yml`: workflow de referencia da aula.
- `ci_fundamentals.py`: resume triggers, jobs, matriz de versoes e comandos locais.
- `01_fundamentos_ci_local.ipynb`: notebook para explorar o contrato do workflow no ambiente local.

## Observacoes didaticas

- CI em ML nao valida apenas codigo; valida tambem reproducibilidade e compatibilidade do ambiente;
- a matriz `3.11` e `3.12` reduz surpresa entre dev local e execucao remota;
- o contrato local deve ser pequeno o bastante para rodar antes do push.