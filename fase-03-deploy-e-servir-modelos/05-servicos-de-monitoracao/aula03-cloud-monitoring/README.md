# Aula 03 - Cloud monitoring em multiplos provedores

Pacote canonico local para comparar servicos gerenciados de monitoramento em AWS, GCP e Azure. O material foca estrategia de provider, nao credenciais ou provisionamento real.

## Objetivo didatico

- comparar stacks gerenciadas de monitoramento por provedor;
- destacar o melhor encaixe para logs, metricas e alertas em cada caso;
- preservar uma estrutura unica de comparacao local.

## O que foi preservado

- comparativo entre servicos equivalentes de cloud monitoring;
- recomendacoes por cenario de uso;
- abordagem por estrategia para evitar condicionais espalhadas.

## O que foi simplificado

- sem chamadas de API cloud;
- sem dashboards ou alarms reais;
- apenas comparacao local e deterministica.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/05-servicos-de-monitoracao/aula03-cloud-monitoring
python cloud_monitoring_comparison.py
```

## Arquivos

- `cloud_monitoring_comparison.py`: compara provedores de monitoring com o mesmo contrato de estrategia.

## Observacoes didaticas

- a comparacao por estrategia ajuda a enxergar equivalencias entre clouds;
- servico gerenciado reduz operacao, mas altera custo e lock-in;
- observabilidade de ML exige olhar alem de CPU e memoria.