# Tutorial — Do Notebook ao Projeto de Software

> **Objetivo**: refatorar o notebook `notebooks/california-housing-prediction.ipynb` em um projeto Python modular, testável e reproduzível, aplicando SOLID, PEP 8, testes automatizados e práticas mínimas de MLOps.

Cada passo abaixo corresponde a um arquivo do projeto. A ordem é lógica: **scaffold → contrato de dados → domínio → orquestração → CLI → testes → automação**.

> **Como ler este tutorial**: cada passo começa com **o que existe**, segue com **por que essa decisão foi tomada** (com referências oficiais) e termina com **qual anti-pattern estamos evitando**. Se você só quer rodar, pule para o [Passo 16](#passo-16--executar-o-pipeline-ponta-a-ponta).

---

## Passo 0 — Ponto de partida: o notebook

O arquivo [notebooks/california-housing-prediction.ipynb](notebooks/california-housing-prediction.ipynb) representa o trabalho típico de um cientista de dados em fase exploratória. Ele "funciona", mas carrega vários problemas que impedem o uso em produção:

| Problema no notebook | Por que é grave em produção |
|---|---|
| Célula gigante mistura limpeza, features, split, treino e avaliação | Viola **Single Responsibility Principle (SRP)**: qualquer mudança quebra tudo, qualquer teste vira teste de integração lento. |
| `StandardScaler.fit(X)` **antes** do `train_test_split` | **Data leakage**: estatísticas do conjunto de teste vazam para o treino, inflando métricas. Ver [scikit-learn — Common pitfalls: Data leakage](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage). |
| Magic numbers (`5.0`, `0.001`, `200`, `0.2`, `42`) sem nome | Anti-pattern clássico ([Magic Number — Refactoring.Guru](https://refactoring.guru/smells/magic-numbers)): impossível saber a intenção sem rodar o código. |
| `print(...)` em vez de `logging` | Sem nível, sem timestamp, sem destino configurável. A [documentação oficial do `logging`](https://docs.python.org/3/howto/logging.html#when-to-use-logging) recomenda explicitamente substituir `print` por `logging` em qualquer código além de scripts triviais. |
| `pickle.dump` em path hardcoded `best_model.pkl` | Caminho fixo torna o código não-portável, impede injeção de outro destino (S3, GCS) e dificulta testes. Ver também os [security warnings oficiais do `pickle`](https://docs.python.org/3/library/pickle.html#module-pickle). |
| Dicionário de modelos hardcoded | Adicionar um modelo novo exige editar a célula central — fere o **Open/Closed Principle (OCP)**. |
| Sem validação de schema, sem testes, sem CLI | Erros silenciosos, regressões não detectadas, execução manual. |

**Referência geral sobre o problema**: [Hidden Technical Debt in Machine Learning Systems (Sculley et al., NeurIPS 2015)](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html) — o paper que cunhou a expressão "ML code is a tiny fraction of a real ML system".

---

## Passo 1 — `pyproject.toml`: contrato do projeto

O [pyproject.toml](pyproject.toml) é hoje o **único** arquivo de configuração padronizado para projetos Python. Ele substitui a combinação histórica `setup.py` + `setup.cfg` + `requirements.txt` + `MANIFEST.in`.

### Por que `pyproject.toml`?

- Padronizado pelas PEPs oficiais:
  - [PEP 517 — A build-system independent format for source trees](https://peps.python.org/pep-0517/)
  - [PEP 518 — Specifying minimum build system requirements](https://peps.python.org/pep-0518/)
  - [PEP 621 — Storing project metadata in `pyproject.toml`](https://peps.python.org/pep-0621/)
- Documentação canônica de uso: [Python Packaging User Guide — Writing your `pyproject.toml`](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/).
- Permite declarar **build backend** (hatchling, setuptools, poetry-core, pdm-backend), **dependências**, **extras**, **entry points** e **configuração de ferramentas** (`ruff`, `pytest`, `mypy`) num único lugar.

### Anti-pattern evitado

Misturar `requirements.txt` (sem versão de Python, sem extras) + `setup.py` executável (que pode rodar código arbitrário em `pip install`) + ferramentas configuradas em arquivos espalhados (`.flake8`, `pytest.ini`, `mypy.ini`).

### Seções principais do nosso `pyproject.toml`

- **`[project]`** — nome, versão, Python mínimo, dependências de runtime (5 libs do notebook + `pandera`, `pydantic`, `pydantic-settings`, `typer`).
- **`[project.optional-dependencies] dev`** — `pytest`, `ruff`, `pre-commit`, `jupyterlab`, `ipykernel`, `matplotlib`, `seaborn`. A separação runtime/dev evita inflar a imagem Docker em produção.
- **`[project.scripts] ml-pipeline`** — instala um comando de terminal apontando para `ml_pipeline.cli:app`. Ver [Entry points specification](https://packaging.python.org/en/latest/specifications/entry-points/).
- **`[build-system]`** — usa [`hatchling`](https://hatch.pypa.io/latest/) (moderno, rápido, recomendado pela PyPA).
- **`[tool.ruff]`** — regras de lint (PEP 8 + isort + pyupgrade + bugbear + simplify + pydocstyle).
- **`[tool.pytest.ini_options]`** — adiciona `src/` ao `pythonpath`.

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

**O que cada flag faz**:
- `-e` (editable, [PEP 660](https://peps.python.org/pep-0660/)): mudanças em `src/` refletem imediatamente sem reinstalar.
- `.[dev]`: instala o projeto a partir do diretório atual com o extra `dev`.
- O comando `ml-pipeline` fica disponível no `PATH` do venv.

### Verificar

```bash
which python              # .../venv/bin/python
which ml-pipeline         # .../venv/bin/ml-pipeline
python -c "import ml_pipeline; print(ml_pipeline.__file__)"
```

---

## Passo 2 — `src/ml_pipeline/__init__.py`: marca o pacote

Arquivo mínimo que declara o pacote Python. Sem ele, `import ml_pipeline` não funciona em namespaces regulares.

### Por que o layout `src/`?

- Recomendação oficial da PyPA: [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/).
- **Anti-pattern (flat layout)**: ter `ml_pipeline/` na raiz faz com que `python` rodado no diretório do projeto importe o código **não instalado**, mascarando bugs de empacotamento (faltando arquivos no wheel, por exemplo).
- Com `src/`, você é obrigado a instalar (`pip install -e .`) para importar — o que reproduz o cenário do usuário final.

---

## Passo 3 — `config.py`: parâmetros centralizados (Pydantic Settings)

Em [src/ml_pipeline/config.py](src/ml_pipeline/config.py), todos os magic numbers do notebook viram campos tipados de `PipelineConfig(BaseSettings)`.

### Por que Pydantic Settings?

- Documentação oficial: [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/).
- Validação automática de tipos (`test_size: float` rejeita `"abc"` em runtime).
- Carrega de **três fontes** com precedência clara: defaults → variáveis de ambiente → kwargs (CLI).
- Padrão alinhado com [The Twelve-Factor App — III. Config](https://12factor.net/config): *"store config in the environment"*.

### Mapeamento

| Magic number do notebook | Campo em `PipelineConfig` |
|---|---|
| `5.0` | `target_upper_clip` |
| `0.2` | `test_size` |
| `42` | `random_state` |
| `'MedHouseVal'` | `target_column` |
| `'best_model.pkl'` (path) | `artifacts_dir / "best_model.pkl"` |

### 3 camadas de configuração (precedência crescente)

1. Defaults no código.
2. Variáveis de ambiente com prefixo `MLPIPE_` (ex.: `MLPIPE_RANDOM_STATE=7`).
3. Flags da CLI (próximo passo).

### Anti-pattern evitado

Espalhar `0.2`, `42` e `5.0` por 4 arquivos diferentes. Quando o pesquisador quiser comparar `random_state=42` vs `random_state=7`, ele teria que fazer find/replace global e torcer pra não esquecer um.

**Princípio aplicado**: SRP — única razão de mudança deste módulo é "parâmetros operacionais".

---

## Passo 4 — `schemas.py`: contrato de dados (pandera)

Em [src/ml_pipeline/schemas.py](src/ml_pipeline/schemas.py), `raw_dataset_schema` declara o que o DataFrame **precisa ter**:

- 8 colunas de feature (tipos e ranges).
- `MedHouseVal` positivo, sem nulos.
- `Latitude` entre 32.0 e 42.5; `Longitude` entre -125.0 e -113.0 (geografia da Califórnia).
- `strict=True`: rejeita colunas extras.
- `coerce=True`: tenta converter tipos automaticamente.

### Por que pandera?

- Documentação oficial: [pandera — Statistical Data Testing](https://pandera.readthedocs.io/).
- Inspirada em [Great Expectations](https://greatexpectations.io/) mas com sintaxe mais leve e integração nativa com `pandas`/`polars`.
- Implementa o conceito de **Design by Contract** ([Bertrand Meyer, 1986](https://en.wikipedia.org/wiki/Design_by_contract)): o schema é o contrato pré-condição da função `load_california_housing`.

### Anti-pattern evitado

No notebook, qualquer `df.columns` errado (ex.: dataset atualizado e a coluna virou `MedHouseValue`) quebra silenciosamente lá no `KeyError` dentro do `train_test_split`, com stack trace inútil. Aqui, o erro estoura **na fronteira do sistema**, com mensagem clara apontando exatamente qual coluna falhou e por quê.

> **Princípio**: *fail fast, fail loud* ([Jim Shore, "Fail Fast"](https://www.martinfowler.com/ieeeSoftware/failFast.pdf), publicado por Martin Fowler).

---

## Passo 5 — `data.py`: carregamento + validação

[src/ml_pipeline/data.py](src/ml_pipeline/data.py) tem **uma única função**: `load_california_housing()`, que realiza as tarefas:

1. Baixa o dataset via `sklearn.datasets.fetch_california_housing(as_frame=True)`.
2. Loga o shape (substitui o `print(df.shape)` do notebook). Ver [Logging HOWTO](https://docs.python.org/3/howto/logging.html).
3. **Valida contra o schema** antes de devolver.

**SRP**: este módulo só muda se a fonte de dados mudar (ex.: passar a ler de S3 ou de uma feature store).

---

## Passo 6 — `preprocessing.py`: limpeza

[src/ml_pipeline/preprocessing.py](src/ml_pipeline/preprocessing.py) extrai a linha do notebook:

```python
df = df[df['MedHouseVal'] < 5.0]  # do notebook
```

…para uma função nomeada e parametrizada:

```python
clip_target_outliers(df, target_column="MedHouseVal", upper=5.0)
```

### Decisões

- **Imutabilidade do input**: não muta o DataFrame de entrada (`.loc[mask].reset_index(drop=True)` retorna cópia). Princípio defendido em [Effective Python — Item 31: Be Defensive When Iterating Over Arguments](https://effectivepython.com/).
- **Nome revela intenção**: `clip_target_outliers` é auto-documentado, ao contrário do filtro inline.
- **Logging do efeito**: registra quantas linhas foram removidas — essencial para auditoria de drift de dados.

### Anti-pattern evitado

Mutação in-place silenciosa do DataFrame, que causa o famoso `SettingWithCopyWarning` do pandas (ver [pandas — Returning a view versus a copy](https://pandas.pydata.org/docs/user_guide/indexing.html#returning-a-view-versus-a-copy)) e bugs reproduzíveis apenas na N-ésima execução do notebook.

**SRP**: muda apenas se a regra de limpeza mudar.

---

## Passo 7 — `features.py`: engenharia de features

[src/ml_pipeline/features.py](src/ml_pipeline/features.py) implementa, em uma função, as 3 features criadas no notebook:

```python
df['rooms_per_household'] = df['AveRooms'] / df['HouseAge'].replace(0, 1)
df['bedrooms_per_room'] = df['AveBedrms'] / df['AveRooms']
df['population_per_household'] = df['Population'] / df['AveOccup']
```

A função `add_engineered_features(df)` possui:

- Constante `EPSILON` para evitar divisão por zero (mais robusto numericamente que `.replace(0, 1)`).
- Tipo de saída garantido como `float64`.
- **Idempotência**: chamar duas vezes produz o mesmo resultado — propriedade verificada em teste e crítica para pipelines retentáveis ([Idempotent Receiver — Martin Fowler](https://martinfowler.com/articles/patterns-of-distributed-systems/idempotent-receiver.html)).

### Anti-pattern evitado

Engenharia de features acoplada ao loop de treino. Quando você precisar **servir** o modelo (inference), vai precisar reaplicar exatamente as mesmas transformações — e se elas estiverem espalhadas em uma célula de Jupyter, boa sorte. Esse é o problema clássico de **training-serving skew** descrito em [Rules of Machine Learning (Google) — Rule #29](https://developers.google.com/machine-learning/guides/rules-of-ml#rule_29_the_best_way_to_make_sure_that_you_train_like_you_serve_is_to_save_the_set_of_features_used_at_serving_time).

---

## Passo 8 — `evaluation.py`: métricas como dados

[src/ml_pipeline/evaluation.py](src/ml_pipeline/evaluation.py) introduz `RegressionMetrics`, um `dataclass(frozen=True)` que carrega RMSE, MAE e R². E `compute_metrics(y_true, y_pred)` que devolve essa estrutura imutável.

### Por que `frozen=True`?

- Documentação: [`dataclasses.dataclass(frozen=True)`](https://docs.python.org/3/library/dataclasses.html#dataclasses.dataclass).
- Métricas são **value objects** ([Martin Fowler — ValueObject](https://martinfowler.com/bliki/ValueObject.html)): identidade dada pelo conteúdo, não devem ser mutadas após cálculo.
- Imutabilidade evita bugs do tipo "alguém zerou o RMSE no meio do pipeline para testar".

### Anti-pattern evitado

Retornar um `dict` `{"rmse": ..., "mae": ...}` — sem tipos, sem autocomplete, sem garantia de chaves presentes, vulnerável a typos (`metrics["rsme"]` retorna `KeyError` apenas em runtime).

---

## Passo 9 — `models.py`: catálogo de modelos (Strategy + OCP)

No notebook, os 5 modelos estavam em um `dict` hardcoded:

```python
models = {'LinearRegression': LinearRegression(), ...}
```

Em [src/ml_pipeline/models.py](src/ml_pipeline/models.py):

- `RegressorFactory` é um [`typing.Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol) (typing estrutural — [PEP 544](https://peps.python.org/pep-0544/)).
- 5 funções `build_*` constroem cada modelo dentro de um [`sklearn.pipeline.Pipeline(scaler, estimator)`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html).
- `MODEL_REGISTRY` é o dicionário `{nome: factory}`.

### SOLID aplicado

- **Strategy Pattern** ([GoF, Design Patterns, 1994](https://en.wikipedia.org/wiki/Strategy_pattern)): cada `build_*` é uma estratégia intercambiável.
- **OCP — Open/Closed Principle** ([Robert C. Martin, "The Open-Closed Principle"](https://web.archive.org/web/20060822033314/http://www.objectmentor.com/resources/articles/ocp.pdf)): o módulo está **aberto para extensão** (basta escrever `build_xgboost(...)` e adicionar 1 linha no registry) e **fechado para modificação** (nenhum outro módulo precisa mudar).

### Por que o `StandardScaler` está dentro do `Pipeline`?

A documentação do scikit-learn é explícita: [Common pitfalls — Data leakage during preprocessing](https://scikit-learn.org/stable/common_pitfalls.html#data-leakage-during-pre-processing). O scaler deve ser fitado **apenas** na partição de treino, e o `sklearn.pipeline.Pipeline` faz isso automaticamente dentro de cada `.fit()`.

### Anti-pattern evitado (do notebook)

```python
# ❌ ERRADO: vaza estatísticas do teste para o scaler
scaler = StandardScaler().fit(X)
X_scaled = scaler.transform(X)
X_train, X_test, ... = train_test_split(X_scaled, y, ...)
```

```python
# ✅ CORRETO: scaler dentro do Pipeline, fitado só no treino
pipe = Pipeline([("scaler", StandardScaler()), ("model", Ridge())])
pipe.fit(X_train, y_train)
```

---

## Passo 10 — `persistence.py`: I/O por interface (DIP + ISP + LSP)

No notebook:

```python
with open('best_model.pkl', 'wb') as f:
    pickle.dump(best, f)
```

Em [src/ml_pipeline/persistence.py](src/ml_pipeline/persistence.py):

- **Dois Protocols pequenos** (princípio **ISP — Interface Segregation**, [Robert C. Martin, "The Interface Segregation Principle"](https://web.archive.org/web/20060822054028/http://www.objectmentor.com/resources/articles/isp.pdf)):
  - `ModelPersister.save(model, destination)`
  - `MetricsWriter.write(payload, destination)`
- **Implementações concretas**:
  - `PickleModelPersister`
  - `JsonMetricsWriter`

### SOLID aplicado

- **DIP — Dependency Inversion Principle** ([Robert C. Martin, "The Dependency Inversion Principle"](https://web.archive.org/web/20110714224327/http://www.objectmentor.com/resources/articles/dip.pdf)): o orquestrador depende apenas dos **protocolos**, não das implementações concretas.
- **LSP — Liskov Substitution Principle** ([Liskov & Wing, "A Behavioral Notion of Subtyping", TOPLAS 1994](https://dl.acm.org/doi/10.1145/197320.197383)): qualquer classe que cumpra o contrato pode substituir a padrão sem quebrar quem chama.
- **ISP**: dois protocolos pequenos em vez de uma `Storage` gorda. Quem só salva métricas não precisa implementar `save_model`.

### Anti-pattern evitado

```python
# ❌ Acoplamento direto: impossível injetar mock, impossível trocar destino
def run():
    ...
    with open('best_model.pkl', 'wb') as f:
        pickle.dump(best, f)
```

```python
# ✅ Inversão: pipeline depende da abstração
def run(persister: ModelPersister):
    ...
    persister.save(best, destination)
```

> **Por que importa**: para testar o pipeline, podemos injetar um `FakePersister` que não toca disco. Em produção, podemos injetar um `S3ModelPersister` sem alterar `pipeline.py`. Veja também [Mark Seemann, "Dependency Injection Principles, Practices, and Patterns"](https://www.manning.com/books/dependency-injection-principles-practices-patterns).

---

## Passo 11 — `training.py`: loop de treino

[src/ml_pipeline/training.py](src/ml_pipeline/training.py) reescreve o `for name, m in models.items()` do notebook como `train_and_evaluate(...)`:

- Itera o `MODEL_REGISTRY`.
- Treina cada um, mede tempo com [`time.perf_counter()`](https://docs.python.org/3/library/time.html#time.perf_counter) (clock monotônico de alta precisão — preferível a `time.time()`, que pode andar para trás se o NTP ajustar o relógio).
- Computa métricas via `compute_metrics`.
- Devolve `list[TrainingResult]` ordenada por RMSE crescente.

`TrainingResult` é outro `dataclass(frozen=True)` carregando `name`, `estimator`, `metrics` e `fit_seconds`.

**SRP**: muda só se a política de comparação entre modelos mudar.

---

## Passo 12 — `pipeline.py`: orquestração com injeção de dependências

[src/ml_pipeline/pipeline.py](src/ml_pipeline/pipeline.py) é a função "orquestradora":

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

### SRP em ação

Este módulo **só coordena**. Toda a lógica de domínio está nos módulos especializados. Se você quiser substituir `train_test_split` por `KFold`, muda **apenas aqui**. Se quiser trocar o critério de "melhor modelo" de RMSE para R², muda **apenas em `training.py`**.

> Leitura recomendada: [Robert C. Martin, "The Clean Architecture"](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html).

---

## Passo 13 — `cli.py`: interface de linha de comando (Typer)

[src/ml_pipeline/cli.py](src/ml_pipeline/cli.py) expõe `app`, um [`typer.Typer`](https://typer.tiangolo.com/). O entry point declarado em `pyproject.toml` (`ml-pipeline = "ml_pipeline.cli:app"`) cria o comando de terminal.

### Por que Typer (e não `argparse`)?

- Construído sobre [`click`](https://click.palletsprojects.com/), mas usa **type hints** Python para gerar a CLI automaticamente.
- Documentação: [Typer — First Steps](https://typer.tiangolo.com/tutorial/first-steps/).
- Reduz boilerplate em ~70% comparado a [`argparse`](https://docs.python.org/3/library/argparse.html).

### Uso

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

### Por que pytest (e não `unittest`)?

- Documentação oficial: [pytest — Get Started](https://docs.pytest.org/en/stable/getting-started.html).
- Sintaxe baseada em `assert` Python (sem `self.assertEqual` verboso).
- [Fixtures](https://docs.pytest.org/en/stable/explanation/fixtures.html) com escopo (`function`, `module`, `session`) — evitam recarregar o dataset 8 vezes.
- Plugins ricos: `pytest-cov`, `pytest-xdist` (paralelização), `pytest-mock`.

### Pirâmide de testes aplicada

Seguimos [Mike Cohn — The Test Pyramid (via Martin Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html):

- **Base (rápidos, muitos)**: `test_features.py`, `test_preprocessing.py`, `test_schemas.py`.
- **Meio**: `test_models.py`, `test_persistence.py`.
- **Topo (poucos, lentos)**: `test_pipeline.py` (smoke real, treina modelos).

### Rodar a suíte

```bash
pytest                       # roda tudo
pytest -q                    # output reduzido
pytest -k features           # só testes que casam com "features"
pytest --cov=ml_pipeline     # com cobertura (precisa de pytest-cov)
```

Esperado: todos os testes passam. O smoke leva alguns segundos (treina os 5 modelos no dataset real).

---

## Passo 15 — `.pre-commit-config.yaml`: automação local

[.pre-commit-config.yaml](.pre-commit-config.yaml) configura hooks que rodam **antes** do commit/push:

- [`ruff`](https://docs.astral.sh/ruff/) (lint, com `--fix`) e `ruff-format` — toda vez que você commita.
- Hooks utilitários: `end-of-file-fixer`, `trailing-whitespace`, `check-yaml`.
- `pytest -q` — apenas no `pre-push` (mais lento, faz sentido só antes de mandar pro remoto).

### Por que `pre-commit`?

- Site oficial: [pre-commit.com](https://pre-commit.com/).
- Garante que **nenhum commit entra no repositório sem passar pelo lint**, evitando o anti-pattern do PR cheio de comentários *"rode o linter, por favor"*.
- Versiona os hooks (`rev:` apontando para tags) — todo dev usa a mesma versão de `ruff`, eliminando o "funciona na minha máquina".
- Os hooks são instalados em `.git/hooks/` e disparam automaticamente em eventos do Git ([Git Hooks — documentação oficial](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)).

### Por que `ruff`?

- Documentação: [Ruff — The Ruff Linter](https://docs.astral.sh/ruff/linter/).
- Substitui `flake8` + `isort` + `pyupgrade` + `pydocstyle` + parte do `bandit` com performance ~100× maior (escrito em Rust).
- Aplica regras da [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/) automaticamente.

### Por que padronizar com PEP 8?

A própria [PEP 8](https://peps.python.org/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds) (citando Guido) defende:

> *"Code is read much more often than it is written."*

Padronização via linter:
- Elimina debates de estilo em code review (libera tempo para discutir lógica).
- Reduz carga cognitiva: o cérebro pula formatação e foca no conteúdo.
- Permite navegação consistente entre projetos.

Complementarmente, [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/) padroniza docstrings.

### Ativar

```bash
pre-commit install                           # hook de pre-commit
pre-commit install --hook-type pre-push      # hook de pre-push
pre-commit run --all-files                   # roda agora em todos os arquivos
pre-commit run ruff --all-files              # roda apenas um hook específico
```

### Como verificar que está triggando

**1. No `git commit`** — provoque uma violação de estilo:

```bash
echo "x=1" > teste_estilo.py     # sem espaço, sem newline final
git add teste_estilo.py
git commit -m "teste pre-commit"
```

Saída esperada:
- `ruff` detecta `E225` (missing whitespace around operator) e tenta autofix.
- `end-of-file-fixer` adiciona `\n` final.
- O commit é **abortado**; você precisa fazer `git add` + `git commit` de novo (agora com os arquivos já corrigidos pelos hooks).

**2. No `git push`** — provoque uma falha de teste:

```bash
git commit -m "teste push" --allow-empty
git push
```

Saída esperada: `pytest -q` roda; se falhar, o push é abortado antes de ir ao remoto.

### Bypass (use com extrema parcimônia)

```bash
git commit --no-verify -m "..."   # pula pre-commit
git push --no-verify              # pula pre-push
```

> **Atenção**: o `--no-verify` deve ser exceção justificada (ex.: hotfix em produção fora do horário). Em time, exija revisão manual quando ele for usado.

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

| O que estava no notebook | Onde ficou no projeto | Princípio aplicado |
|---|---|---|
| Célula gigante de pré-processamento+treino | `preprocessing.py` + `features.py` + `training.py` + `pipeline.py` | SRP |
| `StandardScaler.fit` antes do split | Dentro do `Pipeline(scaler, estimator)` em `models.py` | Sem leakage |
| Magic numbers (`5.0`, `0.2`, `42`, `0.001`, `200`) | `config.py` (campos tipados) e `models.py` (parâmetros nomeados) | Clean Code |
| `print(...)` | `logging.getLogger(__name__).info(...)` em todos os módulos | Logging HOWTO |
| `dict` de modelos hardcoded | `MODEL_REGISTRY` | OCP / Strategy |
| Sem validação | `schemas.py` (pandera) | Design by Contract |
| Sem testes | `tests/` (8 arquivos) | Test Pyramid |
| `pickle.dump('best_model.pkl', ...)` | `ModelPersister` injetado em `pipeline.run` | DIP / ISP / LSP |
| Sem CLI | `cli.py` (Typer) + `ml-pipeline` no terminal | 12-Factor |
| Sem reprodutibilidade | `random_state` propagado via `PipelineConfig` | Reprodutibilidade |

---

## Mapa: requisitos da live → onde foram cobertos

### Conceitos-chave abordados

- **SOLID aplicado a ML** ([Robert C. Martin — SOLID Relevance](https://blog.cleancoder.com/uncle-bob/2020/10/18/Solid-Relevance.html)):
  - **SRP** — cada módulo tem uma única razão de mudança.
  - **OCP** — `MODEL_REGISTRY` em `models.py`.
  - **LSP** — `_InMemoryPersister` em `test_persistence.py` substitui o concreto sem quebra.
  - **ISP** — `ModelPersister` e `MetricsWriter` são protocolos pequenos e separados.
  - **DIP** — `pipeline.run` recebe persisters por injeção.
- **pytest e pandera** — `tests/` + `schemas.py`.
- **ruff e pre-commit** — `pyproject.toml [tool.ruff]` + `.pre-commit-config.yaml`.
- **pyproject.toml** ([PEP 621](https://peps.python.org/pep-0621/)) — local da live, com build-backend, entry point, tool sections.
- **CLI com Pydantic Settings** — `cli.py` (Typer) + `config.py` (`BaseSettings`).

### Exercícios realizados

1. **Refatoramento de pipeline monolítica aplicando SRP** — passos 5 a 12.
2. **Suíte de testes com pytest para pipeline de features** — passo 14, especialmente `test_features.py`.
3. **Configuração de pre-commit hooks com ruff** — passo 15.

---

## Próximos passos sugeridos

- Adicionar [`mlflow`](https://mlflow.org/docs/latest/index.html) para tracking de experimentos.
- Substituir `pickle` por [`joblib`](https://joblib.readthedocs.io/en/stable/persistence.html) (mais robusto para modelos sklearn grandes).
- Containerizar com Dockerfile ([12-Factor App, fator V](https://12factor.net/build-release-run)) — próxima fase do curso.
- Adicionar [GitHub Actions](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-python) rodando `pytest` + `ruff` em PRs.
- Adicionar verificação de tipos com [`mypy`](https://mypy.readthedocs.io/) ou [`pyright`](https://microsoft.github.io/pyright/).

---

## Referências consolidadas

### Empacotamento e ambiente
- [PEP 517](https://peps.python.org/pep-0517/) · [PEP 518](https://peps.python.org/pep-0518/) · [PEP 621](https://peps.python.org/pep-0621/) · [PEP 660](https://peps.python.org/pep-0660/)
- [Python Packaging User Guide](https://packaging.python.org/)
- [src layout vs flat layout](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)

### Estilo e qualidade de código
- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [pre-commit.com](https://pre-commit.com/) · [Git Hooks](https://git-scm.com/book/en/v2/Customizing-Git-Git-Hooks)

### SOLID e arquitetura
- Robert C. Martin: [SRP](https://web.archive.org/web/2006/http://www.objectmentor.com/resources/articles/srp.pdf), [OCP](https://web.archive.org/web/20060822033314/http://www.objectmentor.com/resources/articles/ocp.pdf), [ISP](https://web.archive.org/web/20060822054028/http://www.objectmentor.com/resources/articles/isp.pdf), [DIP](https://web.archive.org/web/20110714224327/http://www.objectmentor.com/resources/articles/dip.pdf)
- [Liskov & Wing, "A Behavioral Notion of Subtyping" (1994)](https://dl.acm.org/doi/10.1145/197320.197383)
- [PEP 544 — Protocols (structural subtyping)](https://peps.python.org/pep-0544/)
- [Martin Fowler — ValueObject](https://martinfowler.com/bliki/ValueObject.html) · [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

### Testes e validação
- [pytest documentation](https://docs.pytest.org/en/stable/)
- [pandera documentation](https://pandera.readthedocs.io/)
- [Practical Test Pyramid (Fowler)](https://martinfowler.com/articles/practical-test-pyramid.html)

### ML específico
- [scikit-learn — Common pitfalls and recommended practices](https://scikit-learn.org/stable/common_pitfalls.html)
- [Hidden Technical Debt in ML Systems (Sculley et al., 2015)](https://papers.nips.cc/paper/2015/hash/86df7dcfd896fcaf2674f757a2463eba-Abstract.html)
- [Rules of Machine Learning (Google)](https://developers.google.com/machine-learning/guides/rules-of-ml)
- [The Twelve-Factor App](https://12factor.net/)
