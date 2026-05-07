# Guia de Navegação

Este repositório é uma referência pública para estudantes de Machine Learning Engineering. Leia a estrutura de fora para dentro: fase, disciplina, aula e material de apoio.

## Arco curricular

| Fase | Nome | Papel no programa | Resultado esperado |
| ---- | ---- | ----------------- | ------------------ |
| [01](../fase-01-produtizacao-de-modelos/README.md) | Produtização de Modelos | Construir a base técnica, de produto e de engenharia | Entender o ciclo de vida do modelo e produzir primeiras soluções estruturadas |
| [02](../fase-02-containers-e-ambientes-reprodutiveis/README.md) | Containers e Ambientes Reprodutíveis | Tornar experimentos reproduzíveis e manuteníveis | Empacotar, versionar e operacionalizar dados e modelos |
| [03](../fase-03-cloud-e-mlops/README.md) | Cloud e MLOps | Levar ML para ambientes realistas de execução | Automatizar treino, deploy, serving e observabilidade inicial |
| [04](../fase-04-monitoramento-e-governanca/README.md) | Monitoramento e Governança | Controlar risco, qualidade e confiabilidade | Monitorar drift, validar dados e formalizar compliance operacional |
| [05](../fase-05-deploy-avancado-de-ia-generativa/README.md) | Deploy Avançado de IA Generativa | Aplicar engenharia de ML a sistemas generativos | Servir, avaliar, escalar e proteger aplicações com LLMs e agentes |

## Como navegar

1. Comece pelo README da fase para entender o objetivo daquele estágio.
2. Abra o README da disciplina para entender relevância profissional, resultados esperados e caminho de aulas.
3. Entre nas pastas de aula depois de ler o README mais próximo.
4. Use lives e grupos de estudo como material de apoio local da fase, não como pacotes separados na raiz.
5. Consulte [CONTRIBUTING.md](../CONTRIBUTING.md) antes de adicionar material novo.

## Visão por fase

| Fase | Disciplinas | Ênfase atual |
| ---- | ----------- | ------------ |
| [01](../fase-01-produtizacao-de-modelos/README.md) | 5 | Fundamentos de modelagem, engenharia de software, APIs e SDKs internos |
| [02](../fase-02-containers-e-ambientes-reprodutiveis/README.md) | 4 | Clean code, ambientes, containers, DVC e MLflow |
| [03](../fase-03-cloud-e-mlops/README.md) | 6 | Cloud deployment, CI/CD, pipelines automatizados, monitoramento e performance |
| [04](../fase-04-monitoramento-e-governanca/README.md) | 6 | Drift, qualidade de dados, observabilidade, compliance e inferência causal |
| [05](../fase-05-deploy-avancado-de-ia-generativa/README.md) | 5 | Serving de LLMs, agentes, escalabilidade, avaliação e segurança |

## Material de apoio

Lives e grupos de estudo ficam perto da fase ou disciplina que apoiam:

- phase study groups: `fase-*/grupos-de-estudo/`;
- discipline live sessions: `fase-*/*/lives/`;
- study-group live sessions: `fase-*/grupos-de-estudo/*/lives/`.

Os índices transversais estão em [live-session-index.md](live-session-index.md) e [study-group-index.md](study-group-index.md).

## Dependências

As dependências por fase ficam em `constraints/fase01.txt` até `constraints/fase05.txt`. Elas documentam a base de pacotes para executar exemplos quando necessário; não são atalhos de validação nem respostas finais.

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

## Licenciamento

Alguns materiais podem trazer licença local própria, como o complemento de validação de dados. Antes de reutilizar conteúdo fora do contexto didático, confira o arquivo `LICENSE` mais próximo do material e a orientação institucional vigente.
