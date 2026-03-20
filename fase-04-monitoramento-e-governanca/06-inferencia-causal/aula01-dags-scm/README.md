# Aula 01 - DAGs e SCMs com simulacao local

Pacote canonico leve para introduzir grafos causais direcionados e modelos causais estruturais com uma implementacao local e deterministica. O material evita bibliotecas pesadas e concentra a aula em construir o grafo, definir o mecanismo estrutural e comparar intervencoes simples.

## Objetivo didatico

- representar a historia causal de um problema de produto com um DAG pequeno;
- simular intervencoes em um SCM local e observar efeito medio esperado;
- conectar a intuicao do grafo com a linguagem de `do()` usada nas aulas seguintes.

## O que foi preservado

- Builder para montar o grafo de forma explicita;
- Strategy para comparar diferentes intervencoes;
- simulacao deterministica de efeito medio em um conjunto sintetico.

## O que foi simplificado

- sem biblioteca externa de grafos;
- sem prova formal de do-calculus;
- foco em um exemplo compacto com poucas variaveis.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/06-inferencia-causal/aula01-dags-scm
python causal_dags.py
```

## Arquivos

- `causal_dags.py`: builder do grafo causal e simulacao de intervencoes.

## Observacoes didaticas

- a clareza do grafo e mais importante do que a quantidade de variaveis nesta aula;
- o SCM serve para transformar setas em mecanismo gerador de dados;
- a mesma estrutura pode ser expandida nas aulas de uplift e monitoramento prescritivo.