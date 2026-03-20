# Materiais-MLET

> Clone canônico executável da **Pós-Tech Machine Learning Engineering**. Esta árvore concentra exemplos, demos, notebooks, scripts e pacotes de apoio usados para transformar ementa em prática reprodutível.

---

## Papel deste repositório

Este clone existe para cumprir uma função objetiva: ser a camada de verdade executável do curso. Em vez de centralizar regras acadêmicas, agendas e políticas, ele organiza o que o aluno, o professor e a coordenação precisam para abrir uma fase, entrar em uma disciplina e encontrar rapidamente o fluxo técnico de estudo, demonstração e reaproveitamento.

Na prática, isso significa que o repositório deve responder a quatro perguntas sem ambiguidade:

1. Em que ponto da jornada de ML Engineering esta fase se encaixa.
2. Qual disciplina cobre qual competência profissional.
3. Como navegar do contexto conceitual para o artefato executável.
4. Onde termina a documentação pedagógica local e onde começa a governança canônica do programa.

## Arco curricular

| Fase | Nome | Papel na formação | Resultado esperado |
| ---- | ---- | ----------------- | ------------------ |
| [01](fase-01-fundamentos-de-ml/README.md) | Fundamentos de ML | construir base técnica, de produto e de engenharia | entender o ciclo de vida do modelo e produzir primeiras soluções estruturadas |
| [02](fase-02-feature-engineering-versionamento/README.md) | Feature Engineering e Versionamento | tornar experimentos reprodutíveis e sustentáveis | empacotar, versionar e operacionalizar ativos de dados e modelos |
| [03](fase-03-deploy-e-servir-modelos/README.md) | Deploy e Servir Modelos | levar ML para ambientes de execução reais | automatizar treino, deploy, serving e observabilidade inicial |
| [04](fase-04-monitoramento-e-governanca/README.md) | Monitoramento e Governança | controlar risco, qualidade e confiabilidade | monitorar deriva, validar dados e formalizar compliance operacional |
| [05](fase-05-llms-e-agentes/README.md) | LLMs e Agentes | aplicar a base de engenharia a sistemas generativos | servir, avaliar, escalar e proteger aplicações com LLMs e agentes |

## Como navegar

1. Comece pelo README da fase para entender o objetivo daquela etapa da formação.
2. Entre no README da disciplina para ler relevância profissional, resultados esperados e o caminho de uso do material.
3. Só depois desça para as pastas de aula, que são o nível de execução fina.
4. Use os READMEs como índice pedagógico; use scripts, notebooks e pacotes como evidência executável.

## Verdade executável versus governança canônica

| Camada | O que vive aqui | O que consultar |
| ------ | --------------- | --------------- |
| Verdade executável | notebooks, scripts, exemplos, pacotes, overlays de aula e referências técnicas | este clone e os READMEs locais |
| Governança canônica | políticas, processos, rubricas, precedência documental e regras acadêmicas | [governanca/README.md](../../governanca/README.md) no repositório principal |

Este repositório não replica a governança integral para evitar drift documental. Quando uma decisão depender de regra oficial, prevalece a documentação canônica do programa, especialmente o [Guia de Materiais Técnico-Pedagógicos Executáveis](../../governanca/04-guias/07-guia-de-materiais-tecnico-pedagogicos-executaveis.md), o [Guia de Referenciais Teóricos por Disciplina](../../governanca/04-guias/08-guia-de-referenciais-teoricos-por-disciplina.md) e o [Resumo dos Tech Challenges](../../governanca/resumo-tech-challenges.md).

## Visão por fase

| Fase | Disciplinas | Ênfase executável atual |
| ---- | ----------- | ----------------------- |
| [01](fase-01-fundamentos-de-ml/README.md) | 5 | fundamentos de modelagem, engenharia de software, APIs e SDKs internos |
| [02](fase-02-feature-engineering-versionamento/README.md) | 4 | clean code, ambientes, conteinerização e versionamento com DVC e MLflow |
| [03](fase-03-deploy-e-servir-modelos/README.md) | 6 | deploy em nuvem, CI/CD, pipelines automatizados, monitoramento e performance |
| [04](fase-04-monitoramento-e-governanca/README.md) | 6 | drift, qualidade de dados, observabilidade, compliance e inferência causal |
| [05](fase-05-llms-e-agentes/README.md) | 5 | serving de LLMs, agentes, escalabilidade, avaliação e segurança |

## Curadoria editorial desta clone

- `canonica` é a linha editorial de base para materiais executáveis consolidados.
- `main` deve receber apenas agregações já curadas e aprovadas.
- Materiais migrados entram nas trilhas existentes de fase, disciplina e aula; o objetivo não é importar legado bruto.
- O contexto de bootstrap está em `docs/repository-bootstrap.md`.
- As regras operacionais desta clone local estão em `CONTRIBUTING.md`.

## Setup rápido

### Pré-requisitos

- Python 3.11 ou superior
- [uv](https://docs.astral.sh/uv/) ou pip

### Instalar dependências por fase

```bash
# Apenas uma fase (recomendado)
uv pip install --constraint constraints/fase01.txt --constraint constraints/dev.txt -e ".[fase01,dev]"

# Ou via Makefile
make install-fase01
```

### Instalar tudo

```bash
uv pip install --constraint constraints/fase01.txt --constraint constraints/fase02.txt --constraint constraints/fase03.txt --constraint constraints/fase04.txt --constraint constraints/fase05.txt --constraint constraints/dev.txt -e ".[fase01,fase02,fase03,fase04,fase05,dev]"

# Ou via Makefile
make install
```

## Comandos úteis

```bash
make lint
make format
make test
make validate-bootstrap
make notebooks-check
make clean

# Sem make
python tools/repo_tasks.py validate
python tools/repo_tasks.py notebooks-check
python tools/repo_tasks.py clean
```

Os constraints versionados em `constraints/` fixam o baseline reproduzível por fase e para o ambiente de desenvolvimento.

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
