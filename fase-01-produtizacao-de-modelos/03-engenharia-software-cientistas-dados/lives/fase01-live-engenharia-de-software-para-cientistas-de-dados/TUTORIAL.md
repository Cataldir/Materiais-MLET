# Tutorial — do notebook ao pacote `ml-pipeline`

Refatoramos `notebooks/california-housing-prediction.ipynb` (uma única célula
gigante com várias responsabilidades) num pacote Python pequeno, testado e
com CLI. O foco foi modularizar o código adotando o princípio SRP do SOLID.

> Execute todos os comandos a partir desta pasta:
> `fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados/lives/fase01-live-engenharia-de-software-para-cientistas-de-dados/`.

---

## 1. Setup

```bash
python -m venv venv && source venv/bin/activate
pip install -e ".[dev]"

# Hooks: o .git/ fica na raiz do monorepo, então instale apontando para
# o config desta live (rode da raiz do repositório):
CFG=fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados/lives/fase01-live-engenharia-de-software-para-cientistas-de-dados/.pre-commit-config.yaml
pre-commit install --config "$CFG"
pre-commit install --hook-type pre-push --config "$CFG"
```

Roda o pipeline:

```bash
ml-pipeline                  # treina e salva artifacts/best_model.pkl + metrics.json
ml-pipeline --test-size 0.3
```

Roda os testes:

```bash
pytest -vv
```

---

## 2. Estrutura

```
.
├── pyproject.toml            # metadados, dependências, ruff, pytest
├── .pre-commit-config.yaml   # ruff (commit) + pytest (push)
├── src/ml_pipeline/
│   ├── __init__.py
│   ├── config.py             # PipelineConfig (Pydantic Settings)
│   ├── data.py               # schema pandera + load_data + clip_target
│   ├── features.py           # add_features
│   ├── models.py             # build_models + evaluate + train_and_evaluate
│   ├── pipeline.py           # run() — orquestra tudo
│   └── cli.py                # comando `ml-pipeline`
└── tests/
    ├── conftest.py
    ├── test_data.py
    ├── test_features.py
    ├── test_models.py
    ├── test_pipeline.py
    └── test_cli.py
```

**6 módulos**, **5 testes**. Cada módulo do `src/` corresponde a um teste.

---

## 3. SRP em ação — mapa notebook → projeto

A célula do notebook fazia **tudo**: limpeza, feature engineering,
split, treino, avaliação e persistência. Cada responsabilidade virou um
módulo:

| Trecho do notebook                  | Módulo no projeto               |
| ----------------------------------- | ------------------------------- |
| `fetch_california_housing(...)`     | `data.load_data`                |
| `df = df[df.MedHouseVal < 5]`       | `data.clip_target`              |
| `df['rooms_per_household'] = ...`   | `features.add_features`         |
| dicionário `models = {...}`         | `models.build_models`           |
| loop de fit + métricas              | `models.train_and_evaluate`     |
| `pickle.dump(...)`                  | `pipeline.run`                  |
| (não existia)                       | `cli.app`                       |
| (não existia)                       | `config.PipelineConfig`         |

Por que importa? **Para mudar uma coisa, você abre um arquivo só.** Trocar
o critério de limpeza não afeta a feature engineering nem o treino.

---

## 4. Os 5 pontos do enunciado

### 4.1 SOLID — apenas SRP

Cada módulo tem **uma** responsabilidade clara (ver tabela acima). Não
adicionamos abstrações (Protocols, dataclasses, factories) que não sejam
estritamente necessárias para o tamanho do projeto.

### 4.2 pytest + pandera

- **pandera** valida o dataset assim que ele é carregado:

  ```python
  raw_schema = pa.DataFrameSchema({
      "MedInc": pa.Column(float, pa.Check.gt(0)),
      "Latitude": pa.Column(float, pa.Check.in_range(32, 42)),
      ...
      "MedHouseVal": pa.Column(float, pa.Check.gt(0)),
  })

  def load_data():
      df = fetch_california_housing(as_frame=True).frame
      return raw_schema.validate(df)   # falha cedo se mudar algo
  ```

- **pytest** cobre cada módulo. Exemplo (`tests/test_data.py`):

  ```python
  def test_schema_rejeita_target_negativo(raw_df):
      bad = raw_df.copy()
      bad.loc[0, "MedHouseVal"] = -1.0
      with pytest.raises(SchemaError):
          raw_schema.validate(bad)
  ```

- **`tests/test_pipeline.py`** roda o pipeline inteiro num `tmp_path` e
  verifica `R² > 0.5` e os artefatos no disco — ou seja, é um teste de
  integração simples sem `mock`.

Docs: [pytest](https://docs.pytest.org/), [pandera](https://pandera.readthedocs.io/).

### 4.3 ruff + pre-commit

`pyproject.toml`:

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]
```

Cinco famílias de regras, suficientes para um projeto inicial:

- `E`/`F` — pycodestyle/pyflakes (erros básicos)
- `I` — ordenação de imports
- `UP` — moderniza sintaxe (pyupgrade)
- `B` — bugs comuns (bugbear)

`.pre-commit-config.yaml` (vive nesta pasta; o `.git/` está na raiz do repositório, então instale os hooks apontando para este arquivo — ver passo abaixo):

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.9
    hooks:
      - id: ruff           # lint (commit)
        args: ["--fix"]
        files: ^fase-01-.../lives/fase01-.../(src|tests)/.*\.py$
      - id: ruff-format    # format (commit)
        files: ^fase-01-.../lives/fase01-.../(src|tests)/.*\.py$
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: bash -c 'cd fase-01-.../lives/fase01-... && pytest -q'
        language: system
        pass_filenames: false
        stages: [pre-push]   # roda só no push
```

> O filtro `files:` impede que o ruff toque nos notebooks didáticos
> (que têm "red flags" intencionais como `fit_transform` antes do split).

**Por que dois estágios?** Lint e format são rápidos → rodam em todo
commit. Pytest é mais lento → roda só no push, evitando enviar código
quebrado ao remoto.

Disparos:

```bash
git commit -m "wip"             # dispara ruff
git push                        # dispara pytest
pre-commit run --all-files      # roda manualmente em tudo
```

Docs: [ruff](https://docs.astral.sh/ruff/), [pre-commit](https://pre-commit.com/).

### 4.4 `pyproject.toml`

Arquivo único que descreve o projeto (formato [TOML](https://toml.io)),
padronizado por [PEP 621](https://peps.python.org/pep-0621/).

```toml
[project]
name = "ml-pipeline"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
  "scikit-learn>=1.4",
  "pandas>=2.2",
  "pandera>=0.20",
  "pydantic-settings>=2.2",
  "typer>=0.12",
]

[project.optional-dependencies]
dev = ["pytest>=8.1", "ruff>=0.6", "pre-commit>=3.6", "ipykernel>=6.29"]

[project.scripts]
ml-pipeline = "ml_pipeline.cli:app"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.hatch.build.targets.wheel]
packages = ["src/ml_pipeline"]

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "B"]

[tool.pytest.ini_options]
pythonpath = ["src"]
```

Bloco a bloco:

- **`[project]`** — nome, versão, dependências de runtime.
- **`optional-dependencies.dev`** — ferramentas de desenvolvimento
  (`pip install -e ".[dev]"`).
- **`[project.scripts]`** — cria o comando `ml-pipeline` no PATH após o
  `pip install -e .`, apontando para `app` em `cli.py`.
- **`[build-system]`** — backend de build (hatchling). Sem isso, `pip`
  não sabe construir o pacote.
- **`[tool.hatch...]`** — onde está o código (layout `src/`,
  recomendação da [PyPA](https://packaging.python.org/en/latest/discussions/src-layout-vs-flat-layout/)).
- **`[tool.ruff.lint]`** — conjunto enxuto de regras.
- **`[tool.pytest.ini_options] pythonpath`** — permite rodar `pytest`
  sem precisar instalar o pacote primeiro.

### 4.5 CLI com Pydantic Settings

```python
# config.py
class PipelineConfig(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="MLPIPE_")
    artifacts_dir: Path = Path("artifacts")
    target_column: str = "MedHouseVal"
    target_upper_clip: float = 5.0
    test_size: float = 0.2
    random_state: int = 42
```

```python
# cli.py
@app.command()
def main(test_size: float = 0.2, random_state: int = 42):
    config = PipelineConfig(test_size=test_size, random_state=random_state)
    best = run(config)
    typer.echo(f"Best: {best['name']} | RMSE={best['rmse']:.4f} ...")
```

Três fontes de configuração com precedência clara:

1. **flag CLI** (`--test-size 0.3`)
2. **variável de ambiente** (`MLPIPE_RANDOM_STATE=7`)
3. **default do `PipelineConfig`**

Docs: [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/),
[Typer](https://typer.tiangolo.com/).

---

## 5. Comparativo

| Aspecto             | Notebook                  | Pacote `ml-pipeline`           |
| ------------------- | ------------------------- | ------------------------------ |
| Reprodutibilidade   | rodar célula a célula     | `pip install -e .` + `ml-pipeline` |
| Configuração        | hard-coded                | `PipelineConfig` (env + CLI)   |
| Validação de dados  | nenhuma                   | `pandera`                      |
| Data leakage        | sim (scaler antes do split) | corrigido com `Pipeline`     |
| Testes              | nenhum                    | `pytest` (5 arquivos)          |
| Estilo              | manual                    | `ruff` + `pre-commit`          |
| Adicionar modelo    | editar várias células     | 1 linha em `build_models`      |

## Referências

- [PEP 8](https://peps.python.org/pep-0008/) — estilo
- [PEP 621](https://peps.python.org/pep-0621/) — `pyproject.toml`
- [PyPA Packaging User Guide](https://packaging.python.org/)
- [scikit-learn — Common pitfalls](https://scikit-learn.org/stable/common_pitfalls.html) (data leakage)
- Robert C. Martin — *Clean Code* (SRP)
