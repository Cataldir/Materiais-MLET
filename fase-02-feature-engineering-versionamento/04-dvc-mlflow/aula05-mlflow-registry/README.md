# Aula 05 - Registry local com transicoes de estado

Pack local para estudar registry de modelos mesmo sem servidor MLflow ativo. O script implementa um registry leve em memoria, com transicoes explicitas entre estagios e validacao de promocao.

## Objetivo didatico

- mostrar o papel dos estagios `staging`, `production` e `archived`;
- treinar regras de promocao sem depender da infraestrutura do servidor;
- ligar governance de modelo a um fluxo observavel e testavel.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula05-mlflow-registry
python mlflow_registry.py
```

## Arquivos

- `mlflow_registry.py`: registry local com transicoes de estado e snapshot final.

## Observacoes didaticas

- o demonstrador preserva a semantica do registry sem exigir dependencia externa;
- a promocao explicita de versoes e mais importante do que a UI da ferramenta;
- o pack serve como base para discutir rollback, aprovacao e trilha de auditoria.