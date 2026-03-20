# 02 — Deploy de Agentes com LLMs

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Agentes são a forma mais direta de transformar LLMs em sistemas capazes de agir, consultar contexto e integrar ferramentas. Esta disciplina trata do desenho operacional desses agentes, cobrindo orquestração, RAG, APIs e a passagem de protótipo conversacional para serviço reutilizável.

## O que você deve aprender

- implementar padrões de agente como ReAct e tool use;
- usar frameworks de orquestração como LangChain e LangGraph com senso crítico;
- integrar RAG e ferramentas customizadas ao fluxo do agente;
- expor agentes como APIs e organizar um projeto end-to-end.

## Como usar este material

1. Comece por agentes ReAct para fixar o padrão de raciocínio e ação.
2. Use LangChain e LangGraph como comparação de abstração e orquestração.
3. Avance para RAG e tools quando a base de controle já estiver clara.
4. Feche com o deploy como API e o projeto integrador para consolidar a trilha.

## Como referenciar esta disciplina no repositório

- A referência principal está em `fase-05-llms-e-agentes/02-deploy-agentes-llms/`.
- Para exemplos concretos, cite a aula correspondente ao padrão de agente ou integração desejada.
- O README é a camada de navegação conceitual; scripts e Dockerfile mostram a implementação prática.
- Questões de governança acadêmica e institucional continuam separadas no repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, essa disciplina ajuda a avaliar quando um agente agrega valor e quando apenas adiciona complexidade. Academicamente, ela oferece base para estudar raciocínio orientado a ferramenta, recuperação de contexto e coordenação de passos em sistemas generativos.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-agentes-react/) | Agentes ReAct e tool use | `react_agent.py` |
| [02](aula02-langchain-langgraph/) | LangChain + LangGraph | `langchain_agent.py`, `langgraph_workflow.py` |
| [03](aula03-rag-tools/) | RAG + custom tools | `rag_pipeline.py`, `custom_tools.py` |
| [04](aula04-deploy-agente-api/) | Deploy agente como API FastAPI | `agent_api.py`, `Dockerfile` |
| [05](aula05-projeto-completo/) | Projeto end-to-end | notebook integrador |
