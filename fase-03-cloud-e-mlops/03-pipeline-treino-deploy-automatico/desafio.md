# Desafio — Pipeline de Treino e Deploy Automático

> **Tipo:** Individual · Não obrigatório · Sem nota
> **Limite:** 2 páginas (≈ 1 000 palavras)

---

## 1. Contexto

Uma empresa de logística tem 5 modelos de previsão de demanda que são re-treinados manualmente toda semana por um cientista de dados. O processo leva 2 dias, é propenso a erros e não tem rastreabilidade. O aluno deve projetar uma **DAG Airflow** que automatize ingestão → feature engineering → treino → avaliação → deploy.

## 2. Objetivos de Aprendizagem

| # | Objetivo |
|---|----------|
| O1 | Modularizar pipeline de ML em etapas isoladas com dependências claras. |
| O2 | Implementar DAG Airflow com ≥ 4 tasks encadeadas. |
| O3 | Adicionar quality gate e lógica champion-challenger. |
| O4 | Garantir reprodutibilidade (seeds, versionamento, data contracts). |

## 3. Escopo e Limites

- **Inclui:** DAG Airflow, scripts modulares, quality gate, data contracts.
- **Exclui:** Infraestrutura cloud real; configuração de Kubernetes.

## 4. Requisitos

### Funcionais (RF)
| RF | Descrição |
|----|-----------|
| RF-01 | DAG com ≥ 4 tasks: ingestão, feature engineering, treino, avaliação. |
| RF-02 | Quality gate: modelo só avança se métrica ≥ threshold. |
| RF-03 | Data contract entre etapas (schema validation com Pandera). |

### Não Funcionais (RNF)
| RNF | Descrição |
|-----|-----------|
| RNF-01 | DAG executável localmente via Docker Compose. |
| RNF-02 | Seeds fixados para reprodutibilidade. |

## 5. Passo a Passo (4 etapas)

| Etapa | Ação | Referência |
|-------|------|-----------|
| 1 | Criar scripts modulares: `ingest.py`, `features.py`, `train.py`, `evaluate.py`. | Aulas 01–03 |
| 2 | Montar DAG Airflow com dependências e XCom para passagem de paths. | Aula 05 |
| 3 | Adicionar validação de schema (Pandera) entre etapas e quality gate. | Aula 06 |
| 4 | Implementar lógica champion-challenger com MLflow. | Aula 07 |

## 6. Entregáveis

| # | Artefato | Formato |
|---|---------|---------|
| E1 | DAG Airflow | `dags/ml_pipeline.py` |
| E2 | Scripts modulares | `src/ingest.py`, `src/features.py`, etc. |
| E3 | Docker Compose para Airflow local | `docker-compose.yml` |

## 7. Checklist de Validação

- [ ] DAG com ≥ 4 tasks e dependências explícitas.
- [ ] Scripts modulares com funções separadas.
- [ ] Schema validation (Pandera) entre ingestão e FE.
- [ ] Quality gate: pipeline falha se métrica < threshold.
- [ ] Champion-challenger: novo modelo comparado com atual.
- [ ] Seeds fixados e reprodutibilidade verificada.

## 8. Rubrica de Auto-Avaliação

| Critério | ⭐ Básico | ⭐⭐ Intermediário | ⭐⭐⭐ Avançado |
|----------|----------|-------------------|---------------|
| Pipeline | Script monolítico | DAG com 3 tasks | DAG ≥ 4 tasks + data contracts |
| Quality gate | Sem gate | Threshold fixo | Champion-challenger com MLflow |
| Reprodutibilidade | Sem seeds | Seeds fixados | Seeds + hash de dados + versioning |

## 9. Matriz de Rastreabilidade

| Objetivo | Requisito | Etapa | Entregável | Aulas |
|----------|-----------|-------|------------|-------|
| O1 | RF-01 | 1 | E2 | Aulas 01–03 |
| O2 | RF-01 | 2 | E1 | Aula 05 |
| O3 | RF-02 | 3–4 | E1 | Aulas 06–07 |
| O4 | RF-03 | 3 | E2 | Aula 06 |

## 10. Extensões Opcionais

- Integrar com GitHub Actions para trigger de re-treino via CI (Aula 08).
- Adicionar agendamento cron semanal e notificação Slack.

## 11. Checklist Rápido

- [ ] Li as aulas 01–08.
- [ ] Criei scripts modulares.
- [ ] Montei DAG Airflow.
- [ ] Quality gate + champion-challenger.
- [ ] Data contracts entre etapas.
- [ ] Documento ≤ 2 páginas.
