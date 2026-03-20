# Aula 03 - Preprocessing otimizado

Pacote canonico local para comparar estrategias de preprocessamento preservando equivalencia semantica. O foco e mostrar que latencia total inclui o preprocessamento e que otimizar nao pode mudar o significado do dado.

## Objetivo didatico

- comparar duas estrategias de preprocessamento com a mesma saida semantica;
- validar equivalencia antes de falar em ganho de performance;
- tratar preprocessamento como parte do benchmark de serving.

## O que foi preservado

- comparacao entre baseline e estrategia otimizada;
- verificacao de equivalencia semantica;
- medicao modelada de custo de preprocessamento.

## O que foi simplificado

- sem imagens grandes, GPU ou bibliotecas pesadas;
- sem benchmark de tempo real sujeito a ruido de maquina;
- apenas transformacao textual local e deterministica.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/06-latencia-performance/aula03-preprocessing-otimizado
python optimized_preprocessing.py
```

## Arquivos

- `optimized_preprocessing.py`: compara estrategias locais de preprocessamento com teste de equivalencia.

## Observacoes didaticas

- otimizar sem validar equivalencia e uma regressao escondida;
- custo modelado ajuda a explicar o ganho sem depender do hardware local;
- preprocessamento tambem e parte do contrato de serving.