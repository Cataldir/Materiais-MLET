# mlet-code-samples

> Código de suporte para as aulas da **Pós-Tech Machine Learning Engineering** — FIAP  
> **Exclusivamente** exemplos, demos, notebooks e scripts. Sem materiais administrativos.

---

## Visão Geral

| Fase | Nome | Disciplinas |
|------|------|-------------|
| [01](fase-01-fundamentos-de-ml/README.md) | Fundamentos de ML | 5 · ~26h vídeo |
| [02](fase-02-feature-engineering-versionamento/README.md) | Feature Engineering e Versionamento | 4 · ~18h vídeo |
| [03](fase-03-deploy-e-servir-modelos/README.md) | Deploy e Servir Modelos | 6 · ~23h vídeo |
| [04](fase-04-monitoramento-e-governanca/README.md) | Monitoramento e Governança | 6 · ~28h vídeo |
| [05](fase-05-llms-e-agentes/README.md) | LLMs e Agentes | 5 · ~22h vídeo |

---

## Setup Rápido

### Pré-requisitos

- Python ≥ 3.11
- [uv](https://docs.astral.sh/uv/) (recomendado) ou pip

### Instalar dependências por fase

```bash
# Apenas uma fase (recomendado)
uv pip install -e ".[fase01,dev]"

# Ou via Makefile
make install-fase01
```

### Instalar tudo

```bash
make install
```

---

## Comandos Úteis

```bash
make lint           # Verificar estilo de código (ruff)
make format         # Formatar código automaticamente
make test           # Executar todos os testes
make notebooks-check  # Verificar notebooks
make clean          # Limpar arquivos temporários
```

---

## Estrutura

```
mlet-code-samples/
├── README.md
├── pyproject.toml
├── Makefile
├── .gitignore
├── .pre-commit-config.yaml
├── fase-01-fundamentos-de-ml/
├── fase-02-feature-engineering-versionamento/
├── fase-03-deploy-e-servir-modelos/
├── fase-04-monitoramento-e-governanca/
└── fase-05-llms-e-agentes/
```

---

## Convenções

- **Scripts Python**: `snake_case.py` com docstring de módulo + Google-style docstrings + type hints
- **Notebooks**: `NN_slug_tema.ipynb` — célula 1 = imports, célula 2 = versões, executável top-to-bottom
- **Sem `print()`** → usar `logging` ou `loguru`
- **Seeds fixados** onde houver aleatoriedade
- **Constantes** em `UPPER_SNAKE_CASE`
- **Dados** em `data/` (`.gitignore`) — instruções de download em cada README
- **Modelos** em `models/` (`.gitignore`) — gerados pelos scripts

---

## Datasets Públicos Utilizados

| Dataset | Uso | Origem |
|---------|-----|--------|
| Titanic | Classificação binária | [Kaggle](https://www.kaggle.com/c/titanic) |
| California Housing | Regressão | `sklearn.datasets` |
| Iris | Classificação multi-classe | `sklearn.datasets` |
| Telecom Churn | Classificação + drift | [Kaggle](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) |
| IMDB Reviews | NLP | `datasets` (HuggingFace) |

---

## Licença

MIT
