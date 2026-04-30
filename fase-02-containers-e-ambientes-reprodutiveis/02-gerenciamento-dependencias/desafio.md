# Desafio — Gerenciamento de Dependências em ML

> Atividade individual, não obrigatória e sem pontuação. Objetivo: fixar os conteúdos desenvolvidos durante a disciplina por meio de um projeto hands-on.

---

## 1) Contexto e Problema

Um notebook de ML que funcionava há 3 meses parou de rodar após atualizações de pacotes. Ninguém sabe quais versões eram usadas. Sua missão: **reconstruir o ambiente reprodutível** do projeto usando ferramentas modernas de gerenciamento de dependências, garantindo que funcione em qualquer máquina.

## 2) Objetivos de Aprendizagem

- Diagnosticar problemas de reprodutibilidade causados por dependências *(Aula 01)*.
- Configurar `pyproject.toml` como single source of truth *(Aula 02)*.
- Gerenciar ambientes com Poetry ou uv *(Aula 02)*.
- Implementar lock files e pinagem de versões *(Aula 03)*.

## 3) Escopo e Restrições

- **Inclui:** migração de requirements.txt para Poetry, lock files, variáveis de ambiente.
- **Fora de escopo:** Docker (outra disciplina), CI/CD.

## 4) Requisitos da Solução

### 4.1 Requisitos funcionais
- **RF01:** `pyproject.toml` configurado com dependências de prod e dev separadas.
- **RF02:** Lock file gerado e commitado.
- **RF03:** `.env` para variáveis de ambiente com `python-dotenv`.
- **RF04:** Script de validação que verifica a instalação limpa.

## 5) Etapas do Desafio

1. **Diagnóstico:** listar problemas de reprodutibilidade do projeto original *(Aula 01)*.
2. **Migração:** converter `requirements.txt` para `pyproject.toml` + Poetry *(Aula 02)*.
3. **Pinagem:** gerar lock file, validar instalação do zero *(Aula 03)*.
4. **Variáveis:** externalizar paths e secrets para `.env` *(Aula 03)*.

## 6) Entregáveis

| # | Entregável | Formato |
|---|------------|---------|
| 1 | Projeto com `pyproject.toml` + lock file | Repositório |
| 2 | Script de validação | `scripts/validate_env.py` |

## 7) Critérios de Validação

- [ ] `poetry install` roda sem erros em ambiente limpo?
- [ ] Lock file commitado e consistente?
- [ ] Variáveis de ambiente externalizadas em `.env`?
- [ ] Script de validação confirma instalação?

## 8) Rubrica de Autoavaliação

| Dimensão | Insuficiente | Adequado | Excelente |
|---|---|---|---|
| Reprodutibilidade | requirements.txt solto | Poetry + lock file | + .env + seeds + script de validação |
| Organização | Deps misturadas | Prod/dev separados | + extras opcionais (ex.: gpu) |

## 9) Matriz de Rastreabilidade

| Tópico teórico | Como é exercitado | Evidência |
|---|---|---|
| Problema de reprodutibilidade (Aula 01) | Diagnóstico | Relatório |
| pyproject.toml e Poetry (Aula 02) | Migração | pyproject.toml |
| Lock files e .env (Aula 03) | Pinagem + variáveis | poetry.lock + .env |

## 10) Extensões opcionais

- Comparar Poetry vs. `uv` em tempo de instalação.
- Configurar múltiplos "extras" (ex.: `[gpu]`, `[test]`).

## 11) Checklist rápido

- [ ] pyproject.toml configurado?
- [ ] Lock file gerado?
- [ ] Instala do zero sem erros?
- [ ] .env com variáveis externalizadas?
- [ ] Script de validação funcional?
