# Aula 02 - LangChain e LangGraph sem dependencia remota

Pacote canonico local para comparar um fluxo linear estilo chain com um fluxo em grafo com roteamento explicito, usando ferramentas deterministicamente simuladas.

## Objetivo didatico

- contrastar composicao linear com orquestracao por grafo;
- mostrar como roteamento explicito melhora observabilidade do fluxo;
- manter o mesmo conjunto de ferramentas em ambos os estilos.

## O que foi preservado

- separacao entre planner, tools e etapas de execucao;
- vocabulario de chain, router, node e state;
- comparacao de artefatos de execucao entre abstracoes.

## O que foi simplificado

- dependencias reais de LangChain ou LangGraph;
- chamadas a modelos hospedados;
- persistencia externa de estado.

## Execucao

```bash
cd fase-05-llms-e-agentes/02-deploy-agentes-llms/aula02-langchain-langgraph
python langchain_agent.py
python langgraph_workflow.py
```

## Arquivos

- `langchain_agent.py`: fluxo sequencial estilo chain.
- `langgraph_workflow.py`: fluxo com roteador e grafo deterministico.

## Observacoes didaticas

- o fluxo linear e mais simples de ler quando a tarefa nao bifurca;
- o fluxo em grafo fica melhor quando a escolha de ferramenta depende do estado;
- ambos compartilham as mesmas tools para que a comparacao nao seja enviesada.