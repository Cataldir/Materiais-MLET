# Aula 03 - Alertas para sistemas de ML

Pacote canonico local para avaliar regras de alerta sobre snapshots de metrica. O material usa avaliacao deterministica para mostrar warning e critical sem depender de Alertmanager.

## Objetivo didatico

- traduzir snapshots de metrica em decisoes operacionais;
- comparar regras independentes para latencia, erro e drift;
- mostrar que alertas devem ser deterministas e auditaveis.

## O que foi preservado

- regras separadas por sinal operacional;
- severidades distintas;
- avaliacao sobre snapshots agregados em vez de eventos isolados.

## O que foi simplificado

- sem integrações com pager ou mensageria;
- sem regras dinamicas por ambiente;
- apenas regras locais com biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/04-monitoracao-performance/aula03-alertas
python alert_rules.py
```

## Arquivos

- `alert_rules.py`: regras deterministicas de alerta sobre snapshots de observabilidade.

## Observacoes didaticas

- uma regra por responsabilidade ajuda a evitar ifs monoliticos;
- alertas devem carregar contexto suficiente para tomada de decisao;
- warning e critical existem para reduzir ruido operacional.