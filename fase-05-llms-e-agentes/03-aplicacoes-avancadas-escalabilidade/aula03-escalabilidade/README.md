# Aula 03 - Escalabilidade para inferencia generativa mockada

Pacote canonico leve para demonstrar tradeoffs entre atendimento assincorno direto, fila com workers e batching assincorno sobre um backend de geracao de texto totalmente mockado.

## Objetivo didatico

- explicar diferenca entre concorrencia, fila e batching;
- medir throughput e latencia modelada sem depender de um LLM real;
- manter um fluxo facil de depurar em notebook e script local.

## O que foi preservado

- foco em throughput, custo por lote e latencia media;
- uso de `asyncio` e `Queue` para simular backpressure;
- comparacao entre estrategias de serving com a mesma carga de requests.

## O que foi simplificado

- chamadas a APIs externas de LLM;
- dependencias de mensageria, Redis ou Docker;
- custos de rede e serializacao reais.

## Execucao

```bash
cd fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula03-escalabilidade
python async_inference.py
```

## Arquivos

- `async_inference.py`: compara atendimento assincorno direto, fila com workers e batching.
- `03_escalabilidade_async_batching.ipynb`: notebook didatico com a mesma simulacao.

## Observacoes didaticas

- `async_direct` privilegia simplicidade, mas nao agrega requests;
- `queued_workers` introduz backpressure controlado e separa ingestao de processamento;
- `async_batching` melhora throughput quando o backend aceita lotes maiores.