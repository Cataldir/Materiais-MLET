# Aula 04 - Benchmark completo

Pacote canonico local para consolidar benchmark e regressao sobre uma baseline versionada. O material evita medições ruidosas de wall clock e usa numeros deterministas para ensinar comparacao entre cenarios.

## Objetivo didatico

- comparar cenarios de serving ponta a ponta contra uma baseline local;
- produzir um relatorio de regressao claro e reprodutivel;
- consolidar latencia, throughput e custo em uma evidencia unica.

## O que foi preservado

- baseline versionada de benchmark;
- verificacao de regressao por cenario;
- harness unico para consolidar resultados.

## O que foi simplificado

- sem medicao real dependente do hardware da maquina;
- sem A/B testing remoto ou carga concorrente;
- relatorio local e deterministico em JSON.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/06-latencia-performance/aula04-benchmark-completo
python benchmark_harness.py
```

## Arquivos

- `benchmark_harness.py`: executa o harness local e compara contra a baseline.
- `benchmark_baseline.json`: snapshot versionado de referencia para regressao.

## Observacoes didaticas

- baseline commitada ajuda a discutir regressao sem ruido experimental;
- um harness pequeno basta para ensinar interpretacao de resultados;
- benchmark so e util quando o criterio de regressao esta explicito.