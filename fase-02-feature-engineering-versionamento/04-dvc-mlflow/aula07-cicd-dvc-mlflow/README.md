# Aula 07 - CI/CD com DVC e tracking local

Pack leve para discutir pipeline de CI em torno de DVC e tracking sem depender de GitHub Actions rodando de verdade. O script modela as etapas como comandos encadeados, enquanto o workflow YAML explicita a orquestracao esperada.

## Objetivo didatico

- conectar reproducao, validacao e publicacao de artefatos em uma esteira de CI;
- mostrar como a pipeline pode falhar cedo antes de publicar metricas;
- manter um contrato local que possa ser inspecionado e testado offline.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula07-cicd-dvc-mlflow
python ci_pipeline.py
```

## Arquivos

- `ci_pipeline.py`: pipeline local de comandos em modo dry-run.
- `.github/workflows/dvc_mlflow_ci.yml`: exemplo de workflow para CI.

## Observacoes didaticas

- o foco esta na estrutura da esteira, nao na execucao em nuvem;
- o workflow aponta para checagens reprodutiveis e upload de artefatos locais;
- esse padrao prepara a conversa sobre gates, evidencias e rollback de pipeline.