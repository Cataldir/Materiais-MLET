# Aula 01 - Tipos de Drift em dados de ML

Pacote canonico leve para demonstrar, com dados sinteticos, como data drift, concept drift e label drift aparecem em um fluxo de monitoramento local. O foco e tornar a diferenca entre os tres tipos visivel sem depender de servicos externos.

## Objetivo didatico

- comparar distribuicoes de referencia e producao para as mesmas features;
- mostrar quando a mudanca esta nas entradas, na relacao com o target ou na distribuicao das classes;
- oferecer versoes em script e notebook para exploracao local e smoke tests.

## O que foi preservado

- geracao deterministica de cenarios com `numpy` e `pandas`;
- resumo por feature com estatistica KS leve e delta medio;
- comparacao entre data drift, concept drift e label drift no mesmo material.

## O que foi simplificado

- sem dashboards, armazenamento historico ou alertas externos;
- sem dependencia obrigatoria de bibliotecas de monitoramento dedicadas;
- validacao estatistica com aproximacao local suficiente para aula e testes.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula01-tipos-drift
python drift_simulator.py
```

## Arquivos

- `drift_simulator.py`: gera tres cenarios sinteticos e retorna resumos programaticos.
- `01_tipos_drift_local.ipynb`: notebook didatico com a mesma sequencia principal do script.

## Observacoes didaticas

- o data drift altera a distribuicao das features observadas;
- o concept drift muda a regra que liga features ao target;
- o label drift muda a proporcao entre classes, mesmo com pipeline local e pequeno.