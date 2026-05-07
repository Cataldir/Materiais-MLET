# 📖 Grupo de Estudos 3 — Containerização e Versionamento

> **Fase:** 02 — Containers e Ambientes Reprodutíveis | **Etapa do TC:** 3

---

## 📋 Foco da Sessão

Docker multi-stage + DVC + MLflow integrados em pipeline reprodutível.

**Disciplinas de referência:**
- [`03-docker-kubernetes`](../../03-docker-kubernetes/)
- [`04-dvc-mlflow`](../../04-dvc-mlflow/)

---

## 🎯 Objetivos

- Criar Dockerfile multi-stage: builder (deps) + runtime (app)
- Configurar `docker-compose.yml` com serviço de treino + MLflow server
- Inicializar DVC, versionar dataset e configurar remote
- Construir pipeline DVC (`dvc.yaml`): preprocess → feature_eng → train → evaluate
- Integrar MLflow tracking no pipeline

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Docker: por que containerizar pipelines de ML?
- Multi-stage builds: reduzir tamanho de imagem
- DVC: git para dados — como funciona?
- Pipeline DVC vs. Makefile vs. Airflow: quando usar cada um?

### 2. Exercício Guiado (~40 min)

1. **Dockerfile multi-stage:**
   ```dockerfile
   # Stage 1: Builder
   FROM python:3.11 AS builder
   # instalar deps, copiar código

   # Stage 2: Runtime
   FROM python:3.11-slim AS runtime
   # copiar apenas o necessário do builder
   ```
   - Verificar que imagem final < 1 GB
   - Testar: `docker build -t mlet-recsys .`

2. **Docker Compose:**
   - Serviço `train`: roda pipeline de treinamento
   - Serviço `mlflow`: UI do MLflow na porta 5000
   - Volume compartilhado para artefatos

3. **DVC setup:**
   - `dvc init` no repositório
   - `dvc add data/raw/interactions.csv`
   - Configurar remote (local: `/tmp/dvc-remote` ou S3)
   - `dvc push` para persistir dados

4. **Pipeline DVC:**
   ```yaml
   stages:
     preprocess:
       cmd: python src/preprocess.py
       deps: [data/raw/interactions.csv, src/preprocess.py]
       outs: [data/processed/features.parquet]
     train:
       cmd: python src/train.py
       deps: [data/processed/features.parquet, src/train.py]
       outs: [models/model.pt]
       metrics: [metrics/train_metrics.json]
   ```
   - Testar: `dvc repro`

### 3. Discussão Aberta (~20 min)

- Como lidar com GPUs em Docker? (nvidia-docker)
- DVC remote: S3 vs. GCS vs. local — trade-offs
- Como garantir que `dvc repro` funciona em qualquer máquina?
- Quando o Docker Compose vira "demais" e precisamos de Kubernetes?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 3:** Pipeline reprodutível via `dvc repro` + Docker funcional

- [ ] Dockerfile multi-stage funcional (imagem < 1 GB)
- [ ] Docker Compose com treino + MLflow
- [ ] DVC inicializado com dataset versionado
- [ ] Pipeline DVC com ≥ 3 stages
- [ ] `dvc repro` reproduz pipeline completo
- [ ] MLflow tracking integrado ao pipeline

---

## 📚 Referências

- Material das disciplinas: [`03-docker-kubernetes`](../../03-docker-kubernetes/), [`04-dvc-mlflow`](../../04-dvc-mlflow/)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [DVC Get Started](https://dvc.org/doc/start)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)
