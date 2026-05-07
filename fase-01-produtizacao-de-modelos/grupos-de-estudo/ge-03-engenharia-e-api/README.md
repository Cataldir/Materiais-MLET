# 📖 Grupo de Estudos 3 — Engenharia e API

> **Fase:** 01 — Produtização de Modelos | **Etapa do TC:** 3

---

## 📋 Foco da Sessão

Refatoração profissional do código, construção de API de inferência e empacotamento reutilizável.

**Disciplinas de referência:**
- [`03-engenharia-software-cientistas-dados`](../../03-engenharia-software-cientistas-dados/)
- [`04-apis-inferencia`](../../04-apis-inferencia-modelos/)
- [`05-bibliotecas-internas`](../../05-bibliotecas-internas-sdks/)

---

## 🎯 Objetivos

- Refatorar código de notebooks para módulos (`src/`) com estrutura limpa
- Criar pipeline reprodutível com Scikit-Learn + transformadores custom
- Escrever testes automatizados (pytest): unitários, schema, smoke test
- Construir API FastAPI com `/predict`, `/health` e validação Pydantic
- Adicionar logging estruturado e middleware de latência
- Configurar `pyproject.toml`, `ruff`, Makefile

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Diferença entre código exploratório (notebook) e código de produção
- Princípios SOLID aplicados a ML: Single Responsibility, Dependency Inversion
- O que é uma API REST? Endpoints, verbos HTTP, status codes
- Pydantic: validação de entrada/saída com type safety

### 2. Exercício Guiado (~40 min)

1. **Refatoração:**
   - Extrair preprocessing do notebook para `src/preprocessing.py`
   - Criar `src/model.py` com classe de treinamento/predição
   - Implementar `src/pipeline.py` com sklearn Pipeline + custom transformers
2. **Testes:**
   - Smoke test: modelo carrega e produz output
   - Schema test: validar formato de input com Pandera
   - Unit test: testar transformador individual
3. **API FastAPI:**
   - Endpoint `/predict` recebendo JSON com features
   - Endpoint `/health` retornando status do modelo
   - Validação Pydantic do request body
   - Middleware de logging com tempo de resposta
4. **Configuração:**
   - `pyproject.toml` com dependências e scripts
   - `Makefile` com targets: `lint`, `test`, `run`

### 3. Discussão Aberta (~20 min)

- Como organizar um repositório de ML para produção?
- Quando usar FastAPI vs. Flask vs. BentoML?
- Quantos testes são "suficientes" para um projeto acadêmico?
- Como versionar o modelo junto com a API?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 3:** Repositório refatorado + API funcional + testes passando

- [ ] Código refatorado em módulos `src/`
- [ ] Pipeline sklearn reprodutível
- [ ] ≥ 3 testes automatizados passando
- [ ] API FastAPI com `/predict` e `/health`
- [ ] Logging estruturado (sem `print()`)
- [ ] `pyproject.toml` + `ruff` sem erros
- [ ] `Makefile` com `lint`, `test`, `run`

---

## 📚 Referências

- Material das disciplinas: [`03-engenharia-software-cientistas-dados`](../../03-engenharia-software-cientistas-dados/), [`04-apis-inferencia`](../../04-apis-inferencia-modelos/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic V2 Docs](https://docs.pydantic.dev/latest/)
- [pytest Getting Started](https://docs.pytest.org/en/stable/getting-started.html)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
