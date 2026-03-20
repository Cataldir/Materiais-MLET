# 03 — Pipeline de Treino e Deploy Automático

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Pipelines automatizados são o elo entre experimentação reprodutível e entrega contínua de valor. Esta disciplina trata do encadeamento operacional que move dados, features, treino, avaliação e deploy sem depender de intervenção manual a cada ciclo.

## O que você deve aprender

- entender o papel de pipelines no ciclo de vida de ML;
- comparar orquestração com Airflow e Prefect;
- introduzir conceitos de feature store como infraestrutura de consistência;
- construir um fluxo ponta a ponta que prepare, treine, avalie e publique modelos.

## Como usar este material

1. Use a aula conceitual para alinhar os estágios do pipeline.
2. Compare DAG e flow para entender diferentes estilos de orquestração.
3. Trate a aula de feature store como expansão de maturidade de dado e feature.
4. Execute o pipeline E2E por último para consolidar o encadeamento completo.

## Como referenciar esta disciplina no repositório

- A pasta oficial é `fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/`.
- Cite a aula específica ao discutir orquestração, feature store ou pipeline ponta a ponta.
- O pacote adicional serve como referência complementar de productization.
- Aspectos normativos e avaliativos devem ser consultados na governança principal do curso.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

No ambiente profissional, automação reduz tempo de ciclo, erro operacional e dependência de execução manual. No ambiente acadêmico, a disciplina explicita encadeamentos causais entre entrada, transformação, treino e publicação, algo central para analisar sistemas de ML como processos completos e não eventos isolados.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-conceitos-pipelines/) | Conceitos de pipelines ML | notebook conceitual |
| [02](aula02-airflow-prefect/) | Airflow DAG + Prefect flow | `ml_dag.py`, `ml_flow.py` |
| [03](aula03-feature-store/) | Feature Store com Feast | `feature_store.yaml`, `features.py` |
| [04](aula04-pipeline-e2e/) | Pipeline E2E: prepare → train → evaluate → deploy | `pipeline_e2e.py` |

## Pacotes canônicos adicionais

| Pacote | Origem | Objetivo |
|------|------|---------|
| [referencia-productization-lstm](referencia-productization-lstm/README.md) | `origin/deep-learning` | Referência de API de inferência e quality gate inspirada no fluxo de productization |
