# Navigation

This repository is a student reference surface for the Machine Learning Engineering program. It should be read from the curriculum structure inward: phase, discipline, lesson, then supporting material.

## Curriculum Arc

| Phase | Name | Role in the program | Expected outcome |
| ---- | ---- | ----------------- | ------------------ |
| [01](../fase-01-produtizacao-de-modelos/README.md) | Produtização de Modelos | Build the technical, product, and engineering base | Understand the model lifecycle and produce structured first solutions |
| [02](../fase-02-containers-e-ambientes-reprodutiveis/README.md) | Containers e Ambientes Reprodutíveis | Make experiments reproducible and maintainable | Package, version, and operationalize data/model assets |
| [03](../fase-03-cloud-e-mlops/README.md) | Cloud e MLOps | Move ML into realistic execution environments | Automate training, deployment, serving, and early observability |
| [04](../fase-04-monitoramento-e-governanca/README.md) | Monitoramento e Governança | Control risk, quality, and reliability | Monitor drift, validate data, and formalize operational compliance |
| [05](../fase-05-deploy-avancado-de-ia-generativa/README.md) | Deploy Avançado de IA Generativa | Apply ML engineering to generative systems | Serve, evaluate, scale, and protect LLM and agent applications |

## How To Navigate

1. Start at the phase README to understand the objective of that stage.
2. Open the discipline README to understand the professional relevance, learning outcomes, and lesson path.
3. Enter lesson folders only after reading the nearby README.
4. Treat live sessions and study groups as phase-local supporting material, not as separate top-level packages.

## Phase View

| Phase | Disciplines | Current emphasis |
| ---- | ----------- | ----------------------- |
| [01](../fase-01-produtizacao-de-modelos/README.md) | 5 | Modeling foundations, software engineering, APIs, and internal SDKs |
| [02](../fase-02-containers-e-ambientes-reprodutiveis/README.md) | 4 | Clean code, environments, containers, DVC, and MLflow |
| [03](../fase-03-cloud-e-mlops/README.md) | 6 | Cloud deployment, CI/CD, automated pipelines, monitoring, and performance |
| [04](../fase-04-monitoramento-e-governanca/README.md) | 6 | Drift, data quality, observability, compliance, and causal inference |
| [05](../fase-05-deploy-avancado-de-ia-generativa/README.md) | 5 | LLM serving, agents, scalability, evaluation, and security |

## Supporting Material

Live sessions and study groups live near the phase or discipline they support:

- phase study groups: `fase-*/grupos-de-estudo/`;
- discipline live sessions: `fase-*/*/lives/`;
- study-group live sessions: `fase-*/grupos-de-estudo/*/lives/`.

The cross-cohort indexes are in [live-session-index.md](live-session-index.md) and [study-group-index.md](study-group-index.md).

## Dependency Notes

Phase-specific dependency constraints are kept in `constraints/fase01.txt` through `constraints/fase05.txt`. They document the package baseline for running lesson code when needed; they are not validation shortcuts or answer keys.

## Convenções de material executável

- Scripts Python em `snake_case.py`, com tipagem e docstrings onde fizer sentido didático.
- Notebooks executáveis de cima para baixo, sem depender de estado oculto.
- Logs e rastreamento substituem `print()` em fluxos operacionais.
- Seeds fixados quando houver aleatoriedade relevante para comparação de resultados.
- Dados e modelos gerados não fazem parte do baseline canônico, salvo quando forem amostras didáticas pequenas e explicitamente documentadas.

## Datasets públicos recorrentes

| Dataset | Uso principal | Origem |
| ------- | ------------- | ------ |
| Titanic | classificação binária e baseline tabular | [Kaggle](https://www.kaggle.com/c/titanic) |
| California Housing | regressão | `sklearn.datasets` |
| Iris | classificação multiclasse | `sklearn.datasets` |
| Telecom Churn | classificação, drift e monitoramento | [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| IMDB Reviews | NLP e avaliação | `datasets` (Hugging Face) |

## Licença

MIT
