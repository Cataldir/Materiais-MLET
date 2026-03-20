# Aula 02 - MLflow para monitoramento continuo local

Pacote canonico leve para mostrar como MLflow pode funcionar como trilha de observabilidade de modelos mesmo em um fluxo local, com batches sinteticos, metricas comparaveis e fallback amigavel quando a dependencia nao esta instalada.

## Objetivo didatico

- ligar observabilidade operacional a uma trilha de execucao reproduzivel;
- comparar batches estaveis, de atencao e criticos no mesmo fluxo;
- mostrar como uma ferramenta de tracking pode servir tambem para monitoramento continuo.

## O que foi preservado

- comparacao entre batches com degradacao progressiva;
- papel do tracking de metricas, tags e artefatos de resumo;
- leitura executiva de saude operacional por janela de monitoramento.

## O que foi simplificado

- sem servidor remoto de MLflow como caminho default;
- sem deploy ou integracao com inferencia online real;
- fallback local em JSON para nao bloquear a aula em ambientes enxutos.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/02-ferramentas-monitoramento-modelos/aula02-mlflow-monitoramento
python mlflow_monitoring.py
```

## Arquivos

- `mlflow_monitoring.py`: gera batches sinteticos, registra metricas e resume o status de monitoramento.
- `02_mlflow_monitoramento_local.ipynb`: notebook local com o mesmo fluxo do script.

## Observacoes didaticas

- o valor da aula nao depende de um tracking server remoto; o importante e a disciplina de registrar evidencia observavel;
- batches com drift, erro e latencia mais altos devem ficar claramente separados no resumo final.