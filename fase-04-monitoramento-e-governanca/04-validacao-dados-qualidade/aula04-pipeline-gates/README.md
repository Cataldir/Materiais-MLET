# Aula 04 - Pipeline com gates de qualidade

Pacote canonico local para demonstrar como um pipeline de dados pode bloquear ou liberar lotes com uma decisao `pass`, `warn` ou `fail`. O objetivo e tornar o gate observavel e facil de testar com exemplos sinteticos, sem depender de plataformas externas.

## Objetivo didatico

- transformar checks de qualidade em um contrato objetivo para a esteira;
- combinar missing values, duplicidade e violacoes de faixa em uma decisao unica;
- mostrar diferenca entre lote aceito com observacao e lote bloqueado.

## O que foi preservado

- checks programaticos simples e explicaveis;
- dataclasses como saida estavel para script, notebook e testes;
- exemplos sinteticos cobrindo `pass`, `warn` e `fail`.

## O que foi simplificado

- sem Great Expectations, Pandera ou checkpoint externo;
- sem armazenamento historico e sem orquestrador real;
- regras pequenas e locais para facilitar depuracao em sala.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula04-pipeline-gates
python quality_gates.py
```

## Arquivos

- `quality_gates.py`: gera datasets de exemplo, executa os checks e decide `pass`, `warn` ou `fail`.
- `04_pipeline_gates_local.ipynb`: notebook com a mesma sequencia principal para exploracao local.

## Observacoes didaticas

- `pass` indica lote pronto para seguir a esteira;
- `warn` indica lote liberado com ressalvas e observacao operacional;
- `fail` indica bloqueio do lote antes de treino, scoring ou publicacao de artefato.