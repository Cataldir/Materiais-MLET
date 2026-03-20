# Aula 04 - Projeto de monitoramento

Pacote canonico local que combina coleta, avaliacao de regras e cards operacionais em um unico facade. O objetivo e consolidar os conceitos anteriores em um mini projeto composto.

## Objetivo didatico

- combinar metrica, regra e resumo executivo em um fluxo unico;
- materializar um facade local para monitoração de sistemas de ML;
- mostrar como um projeto pequeno pode evoluir para uma stack maior.

## O que foi preservado

- consolidacao de sinais operacionais;
- status geral do sistema com base em regras;
- visao resumida do sistema para consumo rapido.

## O que foi simplificado

- sem dashboard real, banco temporal ou notificacao externa;
- sem autenticao, multi-tenant ou integracao cloud;
- apenas composicao local e deterministica.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula04-projeto-monitoramento
python monitoring_project.py
```

## Arquivos

- `monitoring_project.py`: facade local que agrega metricas, alertas e cards operacionais.

## Observacoes didaticas

- um facade simples ajuda a esconder o detalhe interno de metricas e regras;
- cards sintetizam o que realmente importa para operacao;
- o mini projeto serve como base para API, dashboard ou automacao real.