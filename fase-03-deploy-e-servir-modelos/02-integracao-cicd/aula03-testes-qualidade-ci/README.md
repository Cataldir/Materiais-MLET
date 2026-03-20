# Aula 03 - Testes e qualidade como gate de CI

Pacote canonico local para enquadrar testes e checks de qualidade como criterio de liberacao em pipelines de integracao continua. A aula mostra que CI util para ML nao roda apenas unit tests: ele protege contrato de dados, comportamento esperado e padrao minimo de entrega.

## Objetivo didatico

- mostrar por que qualidade precisa virar gate automatizado e nao checklist manual;
- combinar testes funcionais, validacao simples de dados e leitura executiva do resultado;
- preparar o aluno para workflows de CI que bloqueiam regressao cedo.

## O que foi preservado

- ideia de gate binario para aprovar ou bloquear mudancas;
- exemplos proximos de um projeto de ML com predicao e checagem de entrada;
- foco em feedback rapido antes de build e deploy.

## O que foi simplificado

- sem dependencia de plataforma de CI ou YAML para executar localmente;
- sem coverage detalhada, matrix de ambiente ou integracao com artefatos externos;
- checks pequenos e explicaveis para facilitar discussao em sala.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula03-testes-qualidade-ci
python ci_quality_tests.py
```

## Arquivos

- `ci_quality_tests.py`: executa testes locais e resume um gate simples de qualidade para CI.
- `03_testes_qualidade_ci_local.ipynb`: notebook local para inspecionar checks e decisao final do gate.

## Observacoes didaticas

- o valor executivo esta em reduzir custo de erro tardio e padronizar criterio de merge;
- um gate pequeno, legivel e rapido tende a ser adotado com mais consistencia.