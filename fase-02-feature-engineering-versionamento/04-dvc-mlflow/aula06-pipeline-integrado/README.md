# Aula 06 - Pipeline integrado com DVC e tracking local

Pack local-first para demonstrar um pipeline integrado de preparo, treino, avaliacao e rastreio. O material evita depender de `dvc repro` ou servidor MLflow ativo, mas preserva a estrutura de `dvc.yaml`, `params.yaml` e scripts separados em `src/`.

## Objetivo didatico

- conectar orquestracao de pipeline e rastreabilidade de experimento;
- mostrar como separar preparo, treino e avaliacao em etapas reutilizaveis;
- manter um fallback local com arquivos pequenos e resultados deterministas.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/aula06-pipeline-integrado
python pipeline_facade.py
```

## Arquivos

- `dvc.yaml`: contrato de estagios do pipeline.
- `params.yaml`: parametros do demonstrador.
- `src/`: scripts de preparo, treino e avaliacao.
- `pipeline_facade.py`: orquestra o fluxo completo em modo local-first.

## Observacoes didaticas

- o tracking e persistido localmente em JSON para manter o pack autonomo;
- o fluxo e pequeno o suficiente para debug, mas completo o suficiente para explicar a integracao;
- a mesma separacao de etapas escala para projetos maiores com DVC e MLflow reais.