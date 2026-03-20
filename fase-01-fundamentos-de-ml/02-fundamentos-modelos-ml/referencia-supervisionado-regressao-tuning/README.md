# Referencia Canonica - Regressao e Tuning

Pacote canonico derivado do ZIP legado `AprendizadoSupervisionado`, com foco no trecho de regressao e ajuste fino que aparece nas aulas 4 e 5.

## O que foi preservado

- fluxo de regressao supervisionada com dataset publico e reprodutivel;
- comparacao entre baseline linear, regularizacao com Ridge e um modelo de arvore com tuning;
- leitura didatica de metricas, importancia de atributos e criterio de selecao do melhor modelo.

## O que foi removido

- imagens soltas e celulas de apoio que nao afetam a execucao;
- dependencias em arquivos locais do branch legado;
- blocos longos de notebook com repeticao de codigo.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/referencia-supervisionado-regressao-tuning
python supervised_regression_tuning.py
```

## Arquivos

- `supervised_regression_tuning.py`: demo reprodutivel com baseline, Ridge e Random Forest com busca de hiperparametros.
- `01_regressao_tuning_housing.ipynb`: notebook compacto com a mesma sequencia principal.

## Observacoes didaticas

- este pack funciona como ponte entre fundamentos de regressao e conversas de tuning e model selection;
- o script foi estruturado para depuracao local, incluindo um gatilho opcional de `breakpoint()`.