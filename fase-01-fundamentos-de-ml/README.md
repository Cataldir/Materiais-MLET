# Fase 01 — Fundamentos de ML

> ~26h vídeo · 5 disciplinas · ~26 aulas

## Disciplinas

| # | Nome | Aulas |
|---|------|-------|
| [01](01-ciclo-de-vida-de-modelos/README.md) | Ciclo de Vida de Modelos | 5 |
| [02](02-fundamentos-modelos-ml/README.md) | Fundamentos de Modelos de ML | 6 |
| [03](03-engenharia-software-cientistas-dados/README.md) | Engenharia de Software para Cientistas de Dados | 5 |
| [04](04-apis-inferencia-modelos/README.md) | APIs para Inferência de Modelos | 4 |
| [05](05-bibliotecas-internas-sdks/README.md) | Bibliotecas Internas e SDKs | 6 |

## Setup

```bash
make install-fase01
# ou
uv pip install -e ".[fase01,dev]"
```

## Datasets desta fase

- **Titanic**: `wget https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv -P data/`
- **California Housing**: disponível via `sklearn.datasets.fetch_california_housing()`
- **Iris**: disponível via `sklearn.datasets.load_iris()`
