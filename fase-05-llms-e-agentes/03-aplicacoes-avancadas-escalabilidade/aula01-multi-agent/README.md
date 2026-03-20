# Aula 01 - Multi-agent com coordenacao deterministica

Pacote canonico para demonstrar coordenacao entre papeis fixos, sem LLM remoto, usando mediator e agentes especialistas locais.

## Objetivo didatico

- separar responsabilidades entre pesquisa, risco e redacao;
- centralizar a coordenacao para evitar acoplamento entre agentes;
- manter a resposta final completamente reprodutivel.

## Execucao

```bash
cd fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula01-multi-agent
python multi_agent_orchestrator.py
```

## Arquivos

- `multi_agent_orchestrator.py`: coordenador, mediador e agentes de papel fixo.

## Observacoes didaticas

- cada agente responde apenas dentro do proprio escopo;
- o mediador organiza a ordem de colaboracao;
- o coordenador monta a resposta final a partir das contribuicoes.