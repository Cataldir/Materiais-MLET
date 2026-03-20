# Aula 04 - Projeto avancado com replay de workload

Projeto integrador local com filas em memoria, replay deterministico de carga e snapshots de estado para mostrar backlog, throughput e reprocessamento.

## Objetivo didatico

- simular workload realista com itens heterogeneos;
- capturar snapshots de fila e processamento;
- analisar como o backlog evolui sem depender de mensageria externa.

## Execucao

```bash
cd fase-05-llms-e-agentes/03-aplicacoes-avancadas-escalabilidade/aula04-projeto-avancado
python advanced_project.py
```

## Arquivos

- `advanced_project.py`: replay local, filas e estado operacional.
- `04_projeto_avancado_local.ipynb`: notebook fino com o mesmo caminho de execucao.

## Observacoes didaticas

- a fila e local para facilitar inspecao de cada etapa;
- snapshots mostram a progressao do backlog;
- o replay ajuda a discutir escalabilidade sem infraestrutura distribuida.