# Aula 01 - Intro ML com Iris

Pacote canonico derivado de `origin/fundamentos-python`, a partir dos notebooks `Introducao_machine_learning.ipynb` e `aula_iris_model.ipynb`.

## O que foi preservado

- carga do dataset Iris via `scikit-learn`;
- separacao treino/teste com estratificacao;
- baseline de classificacao com pipeline de escalonamento e regressao logistica;
- versoes em script e notebook para uso em aula ou estudo local.

## O que foi removido

- celulas de instalacao com `%pip install`;
- exploracoes dispersas de NumPy e Pandas sem relacao direta com o baseline;
- saida acoplada a `print()` e a um kernel especifico.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula01-intro-ml
python iris_intro_ml.py
```

## Arquivos

- `iris_intro_ml.py`: baseline reprodutivel do Iris com metricas e matriz de confusao.
- `01_intro_ml_iris.ipynb`: versao didatica em notebook com a mesma logica principal.

## Observacoes didaticas

- o objetivo aqui e introduzir o fluxo minimo de um modelo supervisionado, nao maximizar performance;
- o dataset vem do proprio `scikit-learn`, entao o pack roda localmente sem variaveis de ambiente ou downloads manuais.