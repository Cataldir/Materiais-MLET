# 03 — Aplicações Avançadas e Escalabilidade

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Sistemas com LLMs e agentes rapidamente encontram limites de estado, concorrência, coordenação e custo. Esta disciplina trata da arquitetura de aplicações mais sofisticadas, nas quais memória, múltiplos agentes e estratégias de escala passam a ser parte do problema principal.

## O que você deve aprender

- organizar fluxos multiagente com coordenação explícita;
- lidar com memória e estado em conversas de longa duração;
- aplicar concorrência, batching e escalabilidade horizontal em workloads generativos;
- integrar essas preocupações em um projeto avançado coerente.

## Como usar este material

1. Comece pela orquestração multiagente para entender divisão de responsabilidades.
2. Em seguida, trate memória e estado como requisitos de produto e não apenas detalhe técnico.
3. Use a aula de escalabilidade para avaliar throughput, latência e custo.
4. Feche no projeto integrador para observar como as peças se conectam.

## Como referenciar esta disciplina no repositório

- O caminho canônico é `fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/`.
- Cite a aula específica quando o assunto for multiagentes, memória ou escalabilidade.
- Este README funciona como índice didático; notebooks e scripts mostram a implementação e os trade-offs.
- A camada normativa e avaliativa permanece fora desta pasta.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática, essa disciplina ajuda a evitar soluções generativas que quebram ao ganhar usuários, contexto ou complexidade. Em termos acadêmicos, ela permite analisar arquitetura distribuída, gerenciamento de estado e coordenação de agentes como problemas centrais de engenharia contemporânea.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-multi-agent/) | Multi-agent: orquestração | `multi_agent_orchestrator.py` |
| [02](aula02-memoria-estado/) | Memória e estado em conversas | `conversation_memory.py` |
| [03](aula03-escalabilidade/) | Async, batching, horizontal scaling | `async_inference.py`, notebook |
| [04](aula04-projeto-avancado/) | Projeto avançado integrador | notebook |
