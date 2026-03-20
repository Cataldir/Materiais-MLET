# Aula 04 - Deploy de agente como API local

Pacote canonico para expor um agente deterministicamente local via FastAPI, com fronteiras hexagonais, base de conhecimento em memoria e trilhas de trace locais.

## Objetivo didatico

- separar portas e adaptadores de um agente simples;
- expor um endpoint HTTP sem depender de servicos externos;
- registrar traces em memoria para auditoria e depuracao.

## O que foi preservado

- fronteira HTTP clara para ingestao e resposta;
- uso de portas para planner, trace e conhecimento;
- preparo para containerizacao local.

## O que foi simplificado

- autenticacao, filas e observabilidade remota;
- banco de dados externo;
- orquestracao com modelos reais.

## Execucao

```bash
cd fase-05-llms-e-agentes/02-deploy-agentes-llms/aula04-deploy-agente-api
python agent_api.py
```

Se FastAPI estiver disponivel, o modulo tambem expoe `create_app()` para uso com Uvicorn.

## Arquivos

- `agent_api.py`: servico local com FastAPI opcional e traces em memoria.
- `Dockerfile`: imagem minima para empacotar a API localmente.

## Observacoes didaticas

- a regra de negocio continua executavel sem subir servidor;
- traces ficam em memoria para facilitar testes de contrato;
- o Dockerfile existe apenas como empacotamento local, sem dependencias de cloud.