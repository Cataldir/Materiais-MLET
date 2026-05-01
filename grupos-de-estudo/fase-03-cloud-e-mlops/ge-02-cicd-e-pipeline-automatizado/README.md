# 📖 Grupo de Estudos 2 — CI/CD e Pipeline Automatizado

> **Fase:** 03 — Cloud e MLOps | **Etapa do TC:** 2

---

## 📋 Foco da Sessão

Automação completa do ciclo de vida do modelo com GitHub Actions e Airflow.

**Disciplinas de referência:**
- [`02-integracao-cicd`](../../../fase-03-cloud-e-mlops/02-integracao-cicd/)
- [`03-pipeline-treino-deploy`](../../../fase-03-cloud-e-mlops/03-pipeline-treino-deploy/)

---

## 🎯 Objetivos

- Construir workflow GitHub Actions: lint → test → train → evaluate → deploy
- Implementar quality gate: pipeline falha se F1 < threshold
- Criar DAG Airflow: ingestão → feature engineering → treino → avaliação
- Implementar champion-challenger: promover modelo apenas se superar atual
- Aplicar data contracts (Pandera) entre etapas do pipeline

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- CI/CD para ML: diferenças em relação a software tradicional
- GitHub Actions: workflows, jobs, steps, secrets
- Airflow: DAGs, operators, scheduling, XCom
- Champion-challenger: como garantir que um novo modelo é melhor?

### 2. Exercício Guiado (~40 min)

1. **GitHub Actions workflow:**
   ```yaml
   name: ML Pipeline
   on: [push, pull_request]
   jobs:
     lint: ...
     test: ...
     train: ...
     evaluate: ...  # quality gate aqui
     deploy: ...    # só se evaluate passar
   ```
   - Configurar secrets para MLflow URI
   - Quality gate: `if metrics.f1 < 0.75: sys.exit(1)`

2. **DAG Airflow:**
   - Task 1: Ingestão de dados (simular com arquivo local)
   - Task 2: Feature engineering (preprocessing)
   - Task 3: Treinamento do modelo
   - Task 4: Avaliação + champion-challenger
   - XCom para passar métricas entre tasks

3. **Data contracts:**
   - Pandera schema entre ingestão → feature engineering
   - Validar: tipos corretos, sem nulls em colunas críticas, ranges válidos
   - Pipeline aborta se contract violado

4. **Champion-challenger:**
   - Carregar modelo "Production" do MLflow Registry
   - Comparar métricas do novo modelo vs. champion
   - Promover apenas se melhor em ≥ 2 métricas

### 3. Discussão Aberta (~20 min)

- GitHub Actions vs. Jenkins vs. GitLab CI: por que Actions para este projeto?
- Airflow: overkill para projeto acadêmico? Alternativas mais leves?
- Como testar DAGs Airflow localmente?
- Data contracts: quando são essenciais vs. overhead?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 2:** Workflow YAML + DAG Airflow + testes automatizados

- [ ] GitHub Actions com ≥ 3 jobs encadeados
- [ ] Quality gate funcional
- [ ] DAG Airflow com ≥ 4 tasks
- [ ] Champion-challenger implementado
- [ ] Data contracts (Pandera) entre etapas
- [ ] Testes automatizados (≥ 3 tipos)

---

## 📚 Referências

- Material das disciplinas: [`02-integracao-cicd`](../../../fase-03-cloud-e-mlops/02-integracao-cicd/), [`03-pipeline-treino-deploy`](../../../fase-03-cloud-e-mlops/03-pipeline-treino-deploy/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Apache Airflow Docs](https://airflow.apache.org/docs/)
- [Pandera Data Validation](https://pandera.readthedocs.io/)
