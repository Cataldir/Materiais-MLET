# Aula 02 - DoWhy e EconML sem dependencias pesadas

Pacote canonico leve para explicar estimacao de efeito causal com dados sinteticos, sem depender de bibliotecas causais externas. A ideia e emular o raciocinio pedagogico de DoWhy e EconML com codigo local, reprodutivel e facil de depurar.

## Objetivo didatico

- gerar um dataset com confundimento observavel e efeito causal conhecido;
- comparar um estimador ingenuo com ajustes mais robustos;
- mostrar como o ajuste por estratos e por regressao reduz vies.

## O que foi preservado

- foco em tratamento, outcome e confundidores observados;
- comparacao entre abordagens de estimacao com o mesmo dataset;
- versoes em script e notebook para aula local.

## O que foi simplificado

- dependencias de `DoWhy`, `EconML` e grafos completos;
- inferencia estatistica pesada e bootstrap extenso;
- qualquer necessidade de ambiente cloud ou datasets externos.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/06-inferencia-causal/aula02-dowhy-econml
python causal_effect_estimation.py
```

## Arquivos

- `causal_effect_estimation.py`: gera dados sinteticos e compara tres estimadores de ATE.
- `02_dowhy_econml_local.ipynb`: notebook didatico com a mesma sequencia do script.

## Observacoes didaticas

- o valor real do efeito causal e conhecido porque os dados sao simulados;
- o estimador ingenuo ignora confundimento e costuma errar mais;
- a regressao ajustada funciona aqui como uma aproximacao local para o raciocinio de bibliotecas causais mais completas.