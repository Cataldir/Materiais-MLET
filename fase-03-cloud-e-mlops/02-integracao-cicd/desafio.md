# Desafio — Integração com CI/CD (GitHub Actions)

> **Tipo:** Individual · Não obrigatório · Sem nota  
> **Limite:** 2 páginas (≈ 1 000 palavras)

---

## 1. Contexto

O time de ML de uma healthtech entrega modelos manualmente: notebooks rodados localmente, modelos copiados via SCP e deploy via SSH. O CTO quer adotar **CI/CD com GitHub Actions** para automatizar lint, testes, treino, registro e deploy de modelos. O aluno deve criar o workflow YAML e os testes.

## 2. Objetivos de Aprendizagem

| # | Objetivo |
|---|----------|
| O1 | Criar workflow GitHub Actions com lint + pytest para projeto de ML. |
| O2 | Adicionar etapa de treino com quality gate (métrica mínima). |
| O3 | Implementar testes de dados, código e modelo. |
| O4 | Configurar deploy condicional com aprovação manual. |

## 3. Escopo e Limites

- **Inclui:** Workflow YAML, testes automatizados, quality gate, deploy staging.
- **Exclui:** Deploy real em nuvem; configuração de infraestrutura.

## 4. Requisitos

### Funcionais (RF)
| RF | Descrição |
|----|-----------|
| RF-01 | Workflow `.github/workflows/ml-pipeline.yml` com ≥ 3 jobs encadeados. |
| RF-02 | Suite de testes: ≥ 1 unitário (preprocessamento), ≥ 1 de dados (schema), ≥ 1 de modelo (smoke test). |
| RF-03 | Quality gate: pipeline falha se F1 < threshold configurável. |

### Não Funcionais (RNF)
| RNF | Descrição |
|-----|-----------|
| RNF-01 | Secrets não devem aparecer no YAML (usar GitHub Secrets). |
| RNF-02 | Workflow deve completar em < 10 min em runner gratuito. |

## 5. Passo a Passo (4 etapas)

| Etapa | Ação | Referência |
|-------|------|-----------|
| 1 | Criar workflow CI: setup Python + lint (ruff) + pytest. | Aula 02 |
| 2 | Adicionar job de treino com log de métricas e quality gate. | Aula 03 |
| 3 | Implementar 3 tipos de testes (unitário, dados, modelo). | Aula 04 |
| 4 | Adicionar job de deploy staging com aprovação via Environment. | Aula 06 |

## 6. Entregáveis

| # | Artefato | Formato |
|---|---------|---------|
| E1 | Workflow YAML completo | `.github/workflows/ml-pipeline.yml` |
| E2 | Suite de testes | `tests/` com ≥ 3 arquivos |
| E3 | README com diagrama do pipeline | Markdown |

## 7. Checklist de Validação

- [ ] Workflow tem ≥ 3 jobs encadeados (build → test → train/deploy).
- [ ] Lint + pytest passando como status checks.
- [ ] Quality gate configurável (threshold em variável).
- [ ] Testes de dados (schema validation) presentes.
- [ ] Smoke test de modelo (carrega e prediz).
- [ ] Secrets usados para credenciais.

## 8. Rubrica de Auto-Avaliação

| Critério | ⭐ Básico | ⭐⭐ Intermediário | ⭐⭐⭐ Avançado |
|----------|----------|-------------------|---------------|
| Workflow | 1 job com lint | ≥ 2 jobs, lint + test | ≥ 3 jobs encadeados com `needs:` |
| Testes | 1 teste unitário | 2 tipos de teste | 3 tipos + smoke test de modelo |
| Deploy | Sem deploy | Deploy sem quality gate | Deploy condicional + approval |

## 9. Matriz de Rastreabilidade

| Objetivo | Requisito | Etapa | Entregável | Aulas |
|----------|-----------|-------|------------|-------|
| O1 | RF-01 | 1 | E1 | Aula 02 |
| O2 | RF-03 | 2 | E1 | Aula 03 |
| O3 | RF-02 | 3 | E2 | Aula 04 |
| O4 | — | 4 | E1 | Aula 06 |

## 10. Extensões Opcionais

- Adicionar build de imagem Docker + push para GHCR no workflow (Aula 05).
- Implementar continuous training com cron schedule (Aula 08).

## 11. Checklist Rápido

- [ ] Li as aulas 01–08.
- [ ] Criei workflow YAML com ≥ 3 jobs.
- [ ] Implementei 3 tipos de testes.
- [ ] Quality gate funcional.
- [ ] Deploy com aprovação.
- [ ] Documento ≤ 2 páginas.
