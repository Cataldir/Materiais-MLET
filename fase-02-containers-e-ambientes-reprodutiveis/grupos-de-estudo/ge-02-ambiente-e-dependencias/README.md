# 📖 Grupo de Estudos 2 — Ambiente e Dependências

> **Fase:** 02 — Containers e Ambientes Reprodutíveis | **Etapa do TC:** 2

---

## 📋 Foco da Sessão

Reprodutibilidade garantida com gerenciamento moderno de dependências: Poetry, lock files e configuração externalizada.

**Disciplina de referência:**
- [`02-gerenciamento-dependencias`](../../02-gerenciamento-dependencias/)

---

## 🎯 Objetivos

- Configurar `pyproject.toml` com Poetry: dependências prod e dev separadas
- Gerar e commitar lock file
- Externalizar configurações para `.env` + Pydantic Settings
- Criar script de validação de ambiente
- Verificar instalação limpa em ambiente novo

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Por que gerenciamento de dependências importa em ML?
- `pyproject.toml` vs. `requirements.txt`: vantagens
- Lock files: garantia de reprodutibilidade
- Variáveis de ambiente vs. hardcoded: segurança e flexibilidade

### 2. Exercício Guiado (~40 min)

1. **Poetry setup:**
   - `poetry init` com metadados do projeto
   - Adicionar deps de produção: `pytorch`, `scikit-learn`, `mlflow`
   - Adicionar deps de dev: `pytest`, `ruff`, `ipykernel`
   - Gerar `poetry.lock`
2. **Configuração externalizada:**
   - Criar `.env.example` com variáveis necessárias
   - Implementar `src/config.py` com Pydantic BaseSettings
   - Carregar: paths de dados, hiperparâmetros, MLflow URI
3. **Validação de ambiente:**
   - Script `scripts/validate_env.py` que verifica:
     - Python version correta
     - Todas as deps instaladas
     - `.env` presente com variáveis obrigatórias
     - GPU disponível (se esperada)
4. **Teste de reprodutibilidade:**
   - Simular: apagar venv, `poetry install`, rodar testes

### 3. Discussão Aberta (~20 min)

- Poetry vs. pip-tools vs. uv: qual escolher e por quê?
- Como lidar com dependências que conflitam (ex.: versões de CUDA)?
- Quando usar Docker vs. apenas Poetry + .env?
- Como gerenciar secrets em projetos acadêmicos?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 2:** Projeto instalável do zero com `poetry install`

- [ ] `pyproject.toml` completo com deps prod/dev
- [ ] `poetry.lock` commitado
- [ ] `.env.example` com todas as variáveis
- [ ] Pydantic Settings para configuração
- [ ] `scripts/validate_env.py` funcional
- [ ] Instalação limpa funciona do zero

---

## 📚 Referências

- Material da disciplina: [`02-gerenciamento-dependencias`](../../02-gerenciamento-dependencias/)
- [Poetry Documentation](https://python-poetry.org/docs/)
- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
