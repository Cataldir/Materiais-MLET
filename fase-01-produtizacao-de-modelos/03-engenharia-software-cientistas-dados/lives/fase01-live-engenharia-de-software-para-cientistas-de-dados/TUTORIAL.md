# Tutorial — Do Notebook ao Projeto de Software

> **Objetivo**: refatorar o notebook `notebooks/california-housing-prediction.ipynb` em um projeto Python modular, testável e reproduzível, aplicando SOLID, PEP8, testes automatizados e práticas mínimas de MLOps.

Cada passo abaixo corresponde a um arquivo do projeto. A ordem é lógica: **scaffold → contrato de dados → domínio → orquestração → CLI → testes → automação**.

---

## Passo 0 — Ponto de partida: o notebook

O arquivo [notebooks/california-housing-prediction.ipynb](notebooks/california-housing-prediction.ipynb) representa o trabalho de um cientista de dados:

- célula gigante mistura limpeza, features, split, treino e avaliação (viola **SRP**).
- `StandardScaler.fit` antes do `train_test_split` causa **data leakage**.
- Magic numbers (`5.0`, `0.001`, `200`, `0.2`, `42`) sem nome ou documentação.
- `print` em vez de `logging`.
- `pickle.dump` em path hardcoded `best_model.pkl`.
- Dicionário de modelos hardcoded.
- Sem validação de schema, sem testes, sem CLI.

---

## Passo 1 — `pyproject.toml`: contrato do projeto

O [pyproject.toml](pyproject.toml) é o **único** arquivo de configuração do projeto. Ele declara:

- **`[project]`** — nome, versão, Python mínimo, dependências de runtime (5 libs do notebook + `pandera`, `pydantic`, `pydantic-settings`, `typer`).
- **`[project.optional-dependencies] dev`** — pytest, ruff, pre-commit, jupyterlab, ipykernel, matplotlib, seaborn.
- **`[project.scripts] ml-pipeline`** — instala um comando de terminal apontando para `ml_pipeline.cli:app`.
- **`[build-system]`** — usa `hatchling` para empacotar.
- **`[tool.ruff]`** — regras de lint (PEP8 + isort + pyupgrade + bugbear + simplify + pydocstyle).
- **`[tool.pytest.ini_options]`** — adiciona `src/` ao `pythonpath` para os testes encontrarem o pacote.

### Criar o venv a partir do `pyproject.toml`

```bash
cd ~/Materiais-MLET/fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados/lives/fase01-live-engenharia-de-software-para-cientistas-de-dados

# 1. Criar o venv
python -m venv venv

# 2. Ativar
source venv/bin/activate

# 3. Atualizar pip
pip install --upgrade pip

# 4. Instalar o projeto em modo editável + extras de desenvolvimento
pip install -e ".[dev]"
```

**O que acontece**:
- `-e` (editable): mudanças em `src/` refletem imediatamente sem reinstalar.
- `.[dev]`: instala o projeto a partir do diretório atual (`.`) com o extra `dev`.
- O comando `ml-pipeline` fica disponível no terminal.

### Verificar

```bash
which python              # .../venv/bin/python
which ml-pipeline         # .../venv/bin/ml-pipeline
python -c "import ml_pipeline; print(ml_pipeline.__file__)"
```

---

## Passo 2 — `src/ml_pipeline/__init__.py`: marca o pacote

Arquivo mínimo que declara o pacote Python. Sem ele, `import ml_pipeline` não funciona.

> **Nota**: o layout `src/ml_pipeline/` (em vez de `ml_pipeline/` na raiz) é a recomendação moderna ([PyPA](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)). Evita que `python` na raiz importe acidentalmente código não instalado.

---

## Passo 3 — `config.py`: parâmetros centralizados (Pydantic Settings)

Em [src/ml_pipeline/config.py](src/ml_pipeline/config.py), todos os magic numbers do notebook viram campos tipados de `PipelineConfig(BaseSettings)`:

| Magic number do notebook | Campo em `PipelineConfig` |
|---|---|
| `5.0` | `target_upper_clip` |
| `0.2` | `test_size` |
| `42` | `random_state` |
| `'MedHouseVal'` | `target_column` |
| `'best_model.pkl'` (path) | `artifacts_dir / "best_model.pkl"` |

**3 camadas de configuração** (precedência crescente):
1. Defaults no código.
2. Variáveis de ambiente com prefixo `MLPIPE_` (ex.: `MLPIPE_RANDOM_STATE=7`).
3. Flags da CLI (próximo passo).

**Princípio aplicado**: SRP — única razão de mudança é "parâmetros operacionais".

---

## Passo 4 — `schemas.py`: contrato de dados (pandera)

Em [src/ml_pipeline/schemas.py](src/ml_pipeline/schemas.py), `raw_dataset_schema` declara o que o DataFrame **precisa ter**:

- 8 colunas de feature (tipos e ranges).
- `MedHouseVal` positivo, sem nulos.
- `Latitude` entre 32.0 e 42.5; `Longitude` entre -125.0 e -113.0 (geografia da Califórnia).
- `strict=True`: rejeita colunas extras.
- `coerce=True`: tenta converter tipos automaticamente.

**Por que importa**: no notebook, qualquer `df.columns` errado quebra silenciosamente lá na frente. Aqui, o erro estoura **na fronteira do sistema**, com mensagem clara.

---

## Passo 5 — `data.py`: carregamento + validação

[src/ml_pipeline/data.py](src/ml_pipeline/data.py) tem **uma única função**: `load_california_housing()`, que realiza as tarefas:

1. Baixa o dataset via `sklearn.datasets.fetch_california_housing(as_frame=True)`.
2. Loga o shape (substitui o `print(df.shape)` do notebook).
3. **Valida contra o schema** antes de devolver.

---

## Passo 6 — `preprocessing.py`: limpeza

[src/ml_pipeline/preprocessing.py](src/ml_pipeline/preprocessing.py) extrai a linha:

```python
df = df[df['MedHouseVal'] < 5.0]  # do notebook
```

…para uma função nomeada e parametrizada:

```python
clip_target_outliers(df, target_column="MedHouseVal", upper=5.0)
```

- Não muta o DataFrame de entrada (`.copy()` implícito via `.loc[mask]`).
- Reseta o índice.
- Loga quantas linhas foram removidas.

**SRP**: muda apenas se a regra de limpeza mudar.

---

## Passo 7 — `features.py`: engenharia de features

[src/ml_pipeline/features.py](src/ml_pipeline/features.py) implementa uma função para as 3 features criadas no notebook:

```python
df['rooms_per_household'] = df['AveRooms'] / df['HouseAge'].replace(0, 1)
df['bedrooms_per_room'] = df['AveBedrms'] / df['AveRooms']
df['population_per_household'] = df['Population'] / df['AveOccup']
```

A função `add_engineered_features(df)` possui:

- Constante `EPSILON` para evitar divisão por zero.
- Tipo de saída garantido como `float64`.
- **Idempotência**: chamar duas vezes produz o mesmo resultado.

---

## Passo 8 — `evaluation.py`: métricas como dados

[src/ml_pipeline/evaluation.py](src/ml_pipeline/evaluation.py) introduz `RegressionMetrics`, um `dataclass(frozen=True)` que carrega RMSE, MAE e R². E `compute_metrics(y_true, y_pred)` que devolve essa estrutura imutável.

**Por que dataclass frozen**: métricas são valores; não devem ser mutadas depois de calculadas.

---

## Passo 9 — `models.py`: catálogo de modelos (Strategy + OCP)

No notebook, os 5 modelos estavam em um `dict` hardcoded:

```python
models = {'LinearRegression': LinearRegression(), ...}
```

Em [src/ml_pipeline/models.py](src/ml_pipeline/models.py):

- `RegressorFactory` é um `Protocol` (typing estrutural).
- 5 funções `build_*` constroem cada modelo dentro de um `sklearn.pipeline.Pipeline(scaler, estimator)`.
- `MODEL_REGISTRY` é o dicionário `{nome: factory}`.

**OCP (Open/Closed)**: adicionar um 6º modelo só exige escrever `build_xgboost(...)` e adicionar 1 linha no registry. Nenhum outro módulo precisa mudar.

**Importante**: o `StandardScaler` agora está **dentro** do `Pipeline`. O scaler é fitado apenas na partição de treino dentro de cada `.fit()`, eliminando o leakage presente no notebook.

---

## Passo 10 — `persistence.py`: I/O por interface (DIP + ISP + LSP)

No notebook:

```python
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best, f)
```

Em [src/ml_pipeline/persistence.py](src/ml_pipeline/persistence.py):

- **Dois Protocols pequenos** (princípio **ISP**):
  - `ModelPersister.save(model, destination)`
  - `MetricsWriter.write(payload, destination)`
- **Implementações concretas**:
  - `PickleModelPersister`
  - `JsonMetricsWriter`

O orquestrador depende apenas dos **protocolos**, não das implementações concretas — isso é **DIP** (Dependency Inversion). Qualquer outra classe que cumpra o contrato pode substituir as padrões — isso é **LSP** (Liskov Substitution).

> **Por que importa**: para testar o pipeline, podemos injetar um `FakePersister` que não toca disco. Em produção, podemos injetar um `S3ModelPersister` sem alterar `pipeline.py`.

---

## Passo 11 — `training.py`: loop de treino

[src/ml_pipeline/training.py](src/ml_pipeline/training.py) reescreve o `for name, m in models.items()` do notebook como `train_and_evaluate(...)`:

- Itera o `MODEL_REGISTRY`.
- Treina cada um, mede tempo com `time.perf_counter()`.
- Computa métricas via `compute_metrics`.
- Devolve `list[TrainingResult]` ordenada por RMSE crescente.

`TrainingResult` é outro `dataclass(frozen=True)` carregando `name`, `estimator`, `metrics` e `fit_seconds`.

---

## Passo 12 — `pipeline.py`: orquestração com injeção de dependências

[src/ml_pipeline/pipeline.py](src/ml_pipeline/pipeline.py) é a função que "orquestra":

```python
def run(
    config: PipelineConfig,
    model_persister: ModelPersister | None = None,
    metrics_writer: MetricsWriter | None = None,
) -> TrainingResult:
```

Sequência:

1. `load_california_housing()` → `clip_target_outliers()` → `add_engineered_features()`.
2. `train_test_split` (apenas split, sem scaler — ele está dentro do Pipeline de cada modelo).
3. `train_and_evaluate(...)` retorna a lista ordenada.
4. Persiste o melhor modelo e o JSON de métricas via injeção.

**SRP**: este módulo **só coordena**. Toda a lógica de domínio está nos módulos especializados.

---

## Passo 13 — `cli.py`: interface de linha de comando (Typer)

[src/ml_pipeline/cli.py](src/ml_pipeline/cli.py) expõe `app`, um `typer.Typer`. O entry point declarado em `pyproject.toml` (`ml-pipeline = "ml_pipeline.cli:app"`) cria o comando de terminal.

**Uso**:

```bash
# Roda com defaults
ml-pipeline

# Sobrescreve via flag
ml-pipeline --test-size 0.3 --random-state 7 --artifacts-dir ./out

# Sobrescreve via env var (prefixo MLPIPE_)
MLPIPE_RANDOM_STATE=99 ml-pipeline
```

A CLI:
1. Configura `logging.basicConfig`.
2. Coleta as flags não-`None` num `dict`.
3. Constrói `PipelineConfig(**overrides)`.
4. Chama `run(config)`.
5. Imprime o resultado final.

---

## Passo 14 — `tests/`: suíte pytest

A pasta [tests/](tests/) contém 8 arquivos:

| Arquivo | Cobre |
|---|---|
| `conftest.py` | Fixtures `raw_dataset` (sessão) e `small_raw_dataset` |
| `test_schemas.py` | pandera aceita o real e rejeita target negativo / latitude inválida |
| `test_preprocessing.py` | `clip_target_outliers` remove certo, reseta índice, não muta input |
| `test_features.py` | 5 asserts: colunas existem, n_linhas igual, idempotência, sem NaN/Inf, dtype float64 |
| `test_models.py` | Registry tem 5, factories devolvem `Pipeline` com scaler+estimator |
| `test_persistence.py` | `PickleModelPersister` round-trip; `JsonMetricsWriter` grava JSON válido; `_InMemoryPersister` prova LSP |
| `test_pipeline.py` | Smoke (R² > 0.5) + injeção de fake persister prova DIP |
| `test_cli.py` | `typer.testing.CliRunner` invoca `app` e valida flags |

### Rodar a suíte

```bash
pytest
```

Esperado: todos os testes passam. O smoke do pipeline leva alguns segundos (treina os 5 modelos no dataset real).

---

## Passo 15 — `.pre-commit-config.yaml`: automação local

[.pre-commit-config.yaml](.pre-commit-config.yaml) configura hooks que rodam **antes** do commit/push:

- `ruff` (lint, com `--fix`) e `ruff-format` — toda vez que você commita.
- Hooks utilitários (end-of-file-fixer, trailing-whitespace, check-yaml).
- `pytest -q` — apenas no `pre-push` (mais lento, faz sentido só antes de mandar pro remoto).

### Ativar

```bash
pre-commit install                           # hooks de commit
pre-commit install --hook-type pre-push      # hook de push
pre-commit run --all-files                   # roda agora em todos os arquivos
```

---

## Passo 16 — Executar o pipeline ponta a ponta

```bash
ml-pipeline --test-size 0.3 --random-state 7
```

Saída esperada:

```
2026-05-07 ... | INFO | ml_pipeline.data | Dataset carregado: 20640 linhas, 9 colunas
2026-05-07 ... | INFO | ml_pipeline.preprocessing | Removidas 965 linhas com MedHouseVal >= 5.00
2026-05-07 ... | INFO | ml_pipeline.training | linear_regression | RMSE=... R2=...
...
2026-05-07 ... | INFO | ml_pipeline.pipeline | Melhor modelo: gradient_boosting (RMSE=...)
Best model: gradient_boosting | RMSE=... MAE=... R2=...
```

Artefatos gerados:

```
artifacts/
├── best_model.pkl
└── metrics.json
```

---

## Mapa: notebook → projeto

| O que estava no notebook | Onde ficou no projeto |
|---|---|
| Célula gigante de pré-processamento+treino | `preprocessing.py` + `features.py` + `training.py` + `pipeline.py` |
| `StandardScaler.fit` antes do split | Dentro do `Pipeline(scaler, estimator)` em `models.py` |
| Magic numbers (`5.0`, `0.2`, `42`, `0.001`, `200`) | `config.py` (campos tipados) e `models.py` (parâmetros nomeados) |
| `print(...)` | `logging.getLogger(__name__).info(...)` em todos os módulos |
| `dict` de modelos hardcoded | `MODEL_REGISTRY` (Strategy/OCP) |
| Sem validação | `schemas.py` (pandera) |
| Sem testes | `tests/` (8 arquivos) |
| `pickle.dump('best_model.pkl', ...)` | `ModelPersister` injetado em `pipeline.run` |
| Sem CLI | `cli.py` (Typer) + `ml-pipeline` no terminal |
| Sem reprodutibilidade | `random_state` propagado via `PipelineConfig` |

---

## Mapa: requisitos da live → onde foram cobertos

### Conceitos-chave abordados

- **SOLID aplicado a ML**:
  - SRP — cada módulo tem uma única razão de mudança.
  - OCP — `MODEL_REGISTRY` em `models.py`.
  - DIP — `pipeline.run` recebe persisters por injeção.
  - ISP — `ModelPersister` e `MetricsWriter` são protocolos pequenos e separados.
  - LSP — `_InMemoryPersister` em `test_persistence.py` substitui o concreto sem quebra.
- **pytest e pandera** — `tests/` + `schemas.py`.
- **ruff e pre-commit** — `pyproject.toml [tool.ruff]` + `.pre-commit-config.yaml`.
- **pyproject.toml** — local da live, com build-backend, entry point, tool sections.
- **CLI com Pydantic Settings** — `cli.py` (Typer) + `config.py` (`BaseSettings`).

### Exercícios realizados

1. **Refatoramento de pipeline monolítica aplicando SRP** — passos 5 a 12.
2. **Suíte de testes com pytest para pipeline de features** — passo 14, especialmente `test_features.py`.
3. **Configuração de pre-commit hooks com ruff** — passo 15.

---

## Próximos passos sugeridos

- Adicionar `mlflow` para tracking de experimentos.
- Substituir `pickle` por `joblib` (mais robusto para modelos sklearn grandes).
- Containerizar com Dockerfile (próxima fase do curso).
- Adicionar GitHub Actions rodando `pytest` + `ruff` em PRs.
