# Aula 04 - MLP estilo PyTorch e Keras com baseline tree-based

Pack canonico leve para comparar duas configuracoes de MLP inspiradas em stacks populares com um baseline tree-based no mesmo problema de classificacao. A aula foca mais no raciocinio de arquitetura de modelos do que na dependencia do framework real.

## O que foi preservado

- comparacao entre abordagens densas e um baseline tipo gradient boosting;
- leitura de trade-offs entre capacidade, regularizacao e estabilidade de treino;
- estrutura adaptada por estrategia para trocar backend sem mudar o fluxo de avaliacao.

## O que foi simplificado

- sem dependencia obrigatoria de PyTorch, TensorFlow ou XGBoost;
- sem GPU, download externo ou tuning pesado;
- foco em experimento local, deterministico e rapido.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/aula04-mlp-pytorch-keras
python mlp_adapter_demo.py
```

## Arquivos

- `mlp_adapter_demo.py`: compara tres estrategias de modelagem com adaptadores leves.

## Observacoes didaticas

- a aula usa o nome dos frameworks como referencia pedagogica de estilo, nao como requisito de runtime;
- o ganho principal e separar o fluxo de avaliacao da escolha do backend do modelo.