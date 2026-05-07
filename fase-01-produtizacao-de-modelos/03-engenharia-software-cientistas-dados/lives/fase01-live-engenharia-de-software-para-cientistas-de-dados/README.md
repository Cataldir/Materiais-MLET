# 📺 Engenharia de Software para Cientistas de Dados

> **Fase:** 01 | **Tipo:** Live de Hands-on

---

## 📋 Contexto

Aplicação de princípios SOLID, testes automatizados, qualidade de código e gestão de dependências em projetos de ciência de dados

**Disciplina de referência:** [`fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados`](../../README.md)

---

## 🎯 Conceitos Abordados

- SOLID aplicado a ML
- pytest e pandera
- ruff e pre-commit
- pyproject.toml
- CLI com Pydantic Settings

---

## 🛠️ Exercícios Práticos

- [ ] Refatorar pipeline monolítico aplicando SRP
- [ ] Criar suíte de testes com pytest para pipeline de features
- [ ] Configurar pre-commit hooks com ruff

---

## 📅 Sessões Realizadas

| Data | Turma | Professor |
|------|-------|----------|
| 07/05/2026 | MLET10 | Erick Muller; Pedro Almeida |

---

## 📁 Estrutura

```text
.
├── README.md                        ← Este arquivo
├── exercicio.py                     ← Script de exercício prático da live
├── TUTORIAL.md                      ← Guia passo a passo de construção do projeto
├── pyproject.toml                   ← Configuração do projeto e dependências
├── .pre-commit-config.yaml          ← Hooks de qualidade de código
├── .gitignore                       ← Arquivos ignorados pelo Git
├── notebooks/
│   ├── california-housing-prediction.ipynb  ← Notebook original (antes da refatoração)
│   └── requirements.txt             ← Dependências mínimas do notebook
├── src/
│   └── ml_pipeline/
│       ├── __init__.py              ← Pacote Python
│       ├── config.py                ← Configuração com Pydantic Settings
│       ├── data.py                  ← Schema (pandera), load e clip do target
│       ├── features.py              ← Engenharia de features
│       ├── models.py                ← Modelos, métricas e treino
│       ├── pipeline.py              ← Orquestração do pipeline
│       └── cli.py                   ← Interface de linha de comando (Typer)
└── tests/
    ├── conftest.py                  ← Fixtures compartilhadas
    ├── test_data.py                 ← Schema + clip
    ├── test_features.py             ← Engenharia de features
    ├── test_models.py               ← Registry e métricas
    ├── test_pipeline.py             ← Integração end-to-end
    └── test_cli.py                  ← CLI
```

---

## 📚 Referências

- Material completo da disciplina: [`fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados`](../../../../fase-01-produtizacao-de-modelos/03-engenharia-software-cientistas-dados/README.md)
- Consulte as aulas da disciplina para aprofundamento em tópicos específicos.
- Google. Machine Learning Crash Course: Framing ML Problems.
- scikit-learn User Guide: model evaluation and metrics.
- Sculley et al. Hidden Technical Debt in Machine Learning Systems.
