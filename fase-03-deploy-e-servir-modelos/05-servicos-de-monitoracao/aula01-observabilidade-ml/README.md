# Aula 01 - Observabilidade para ML

Pacote canonico local para explicar observabilidade de ML por meio de um facade de logs, metricas e traces. A implementacao nao depende de exporters reais, mas preserva a separacao conceitual entre os tres sinais.

## Objetivo didatico

- diferenciar logs, metricas e traces no contexto de inferencia;
- registrar os tres sinais a partir de um unico evento de negocio;
- oferecer um facade simples para evolucao posterior para stacks reais.

## O que foi preservado

- triangulacao entre logs, metricas e traces;
- uma API unica para captura de observabilidade;
- resumo observavel sem infraestrutura externa.

## O que foi simplificado

- sem OpenTelemetry, collector ou backend remoto;
- sem persistencia real de spans;
- apenas estruturas locais e deterministicas.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula01-observabilidade-ml
python ml_observability.py
```

## Arquivos

- `ml_observability.py`: facade local para logs, metricas e traces de inferencia.

## Observacoes didaticas

- logs contam historias detalhadas; metricas resumem comportamento; traces ligam etapas;
- um facade reduz acoplamento com a stack de observabilidade;
- o mesmo evento de negocio pode alimentar os tres sinais ao mesmo tempo.