# Aula 02 - Microservicos, schemas e health checks

Pack canonico para mostrar como contratos explicitos reduzem ambiguidade entre consumidor e servico de inferencia. A aula prioriza estrutura de request/response e checks de saude antes de entrar em uma API completa.

## O que foi preservado

- separacao entre payload externo e objeto de dominio;
- health e readiness como contratos operacionais minimos;
- uso de facade para expor uma interface unica de validacao e predicao.

## O que foi simplificado

- sem servidor HTTP real nem framework web obrigatorio;
- sem dependencia de banco, fila ou registry de servicos;
- foco em schema e contrato, nao em rede.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/04-apis-inferencia-modelos/aula02-microservicos-schemas
python schema_facade_demo.py
```

## Arquivos

- `schema_facade_demo.py`: adapta payloads, valida contratos e devolve respostas padronizadas.

## Observacoes didaticas

- schema bom nao serve apenas para documentar, mas para impedir ambiguidade operacional;
- health e readiness devem ser simples, legiveis e estaveis.