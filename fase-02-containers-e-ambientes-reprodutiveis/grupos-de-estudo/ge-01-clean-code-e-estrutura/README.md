# 📖 Grupo de Estudos 1 — Clean Code e Estrutura

> **Fase:** 02 — Containers e Ambientes Reprodutíveis | **Etapa do TC:** 1

---

## 📋 Foco da Sessão

Projeto limpo com padrões de engenharia de software desde o início: SOLID, naming, type hints e design patterns.

**Disciplina de referência:**
- [`01-clean-code-ml`](../../01-clean-code-ml/)

---

## 🎯 Objetivos

- Definir estrutura de projeto com `src/`, `tests/`, `data/`, `models/`, `configs/`
- Aplicar naming conventions e princípios SOLID
- Implementar ≥ 1 design pattern (Factory, Strategy ou Template Method)
- Type hints em todas as funções públicas + docstrings Google style
- Configurar `ruff` sem erros + pre-commit hooks

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Princípios SOLID: como aplicar em projetos de ML?
- Naming conventions: por que `calculate_feature_importance()` > `calc_fi()`?
- Design Patterns em ML: Factory (criação de modelos), Strategy (preprocessors)
- Type hints: benefícios para manutenção e IDE support

### 2. Exercício Guiado (~40 min)

1. **Estrutura de projeto:**
   - Criar scaffold: `src/`, `tests/`, `data/`, `models/`, `configs/`
   - Definir `__init__.py` com exports públicos
   - Criar `src/models/factory.py` com Factory Pattern para instanciar modelos
2. **Refatoração:**
   - Pegar código "sujo" (funções longas, nomes ruins) e refatorar
   - Aplicar Single Responsibility: 1 função = 1 responsabilidade
   - Adicionar type hints e docstrings Google style
3. **Linting:**
   - Configurar `ruff` no `pyproject.toml`
   - Rodar `ruff check .` e corrigir todos os erros
   - Configurar pre-commit hook para ruff

### 3. Discussão Aberta (~20 min)

- Até onde ir com design patterns em projeto acadêmico?
- Como equilibrar "código limpo" com "entregar rápido"?
- Quais são os code smells mais comuns em projetos de ML?
- Vale a pena abstrair tudo em classes ou funções simples bastam?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 1:** Repositório base com estrutura limpa e linting passando

- [ ] Estrutura `src/`, `tests/`, `data/`, `models/`, `configs/`
- [ ] Naming conventions + SOLID aplicados
- [ ] ≥ 1 design pattern implementado
- [ ] Type hints em todas as funções públicas
- [ ] `ruff check .` sem erros
- [ ] Pre-commit hooks configurados

---

## 📚 Referências

- Material da disciplina: [`01-clean-code-ml`](../../01-clean-code-ml/)
- [Clean Code de Robert C. Martin — Resumo aplicado a Python](https://github.com/zedr/clean-code-python)
- [Ruff Linter](https://docs.astral.sh/ruff/)
