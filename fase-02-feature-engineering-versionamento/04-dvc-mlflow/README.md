# 04 — Controle de Dados e Modelos — DVC + MLflow

> 5h de vídeo · 7 aulas

## Por que esta disciplina importa

Quando dados, parâmetros e modelos não têm rastreabilidade, o projeto perde auditabilidade e se torna difícil de reproduzir ou evoluir. Esta disciplina apresenta as ferramentas centrais para versionar ativos de ML e tornar o experimento uma linha de produção observável.

## O que você deve aprender

- justificar por que versionamento de dados e modelos é parte da solução, não detalhe operacional;
- usar DVC para rastrear datasets, pipelines e estágios de processamento;
- usar MLflow para registrar parâmetros, métricas, artefatos e modelos;
- integrar DVC e MLflow em um fluxo consistente de experimentação e entrega;
- estender esse fluxo para contextos de CI/CD.

## Como usar este material

1. Comece pela motivação do versionamento antes de entrar nas ferramentas.
2. Siga a sequência DVC básico, remoto e tracking no MLflow.
3. Use o pipeline integrado para entender como os componentes se conectam.
4. Explore os pacotes adicionais para ver o padrão aplicado em casos mais próximos de produto.

## Como referenciar esta disciplina no repositório

- O caminho de referência é `fase-02-feature-engineering-versionamento/04-dvc-mlflow/`.
- Ao citar um exemplo, aponte para a aula ou para o pacote canônico adicional correspondente.
- Este README funciona como índice executivo e acadêmico da trilha; arquivos `dvc.yaml`, scripts e exemplos de tracking mostram a materialização da prática.
- Para critérios institucionais de uso e avaliação, consulte a governança principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na rotina profissional, essa disciplina melhora governança de experimentos, recuperação de histórico e diálogo entre ciência, engenharia e operação. No plano acadêmico, ela reforça reprodutibilidade empírica e encadeamento explícito entre hipótese, dado, parâmetro, resultado e artefato final.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-problema-versionamento/) | Por que versionar dados e modelos | notebook |
| [02](aula02-dvc-basico/) | DVC init, track, .dvc files, pipelines | `dvc.yaml`, scripts |
| [03](aula03-dvc-remoto/) | DVC remoto (S3, GCS) + GitHub | scripts de setup |
| [04](aula04-mlflow-tracking/) | MLflow tracking: parâmetros, métricas, artefatos | `mlflow_tracking.py` |
| [05](aula05-mlflow-registry/) | MLflow Model Registry: register + stages | `mlflow_registry.py` |
| [06](aula06-pipeline-integrado/) | Pipeline DVC + MLflow integrado | `dvc.yaml`, `params.yaml`, `src/` |
| [07](aula07-cicd-dvc-mlflow/) | CI/CD com DVC + MLflow | `.github/workflows/` |

## Pacotes canônicos adicionais

| Pacote | Origem | Objetivo |
|------|------|---------|
| [referencia-mlflow-sumarizacao](referencia-mlflow-sumarizacao/README.md) | `origin/mlflow-bentoml` | Tracking local, assinatura de modelo e logging de artefatos para um caso de sumarização |
| [referencia-recomendacao-negocio](referencia-recomendacao-negocio/README.md) | `origin/recommendation-systems` | Caso de negócio com popularidade, features e propensão para recomendação comercial |
