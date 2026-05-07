# 📖 Grupo de Estudos 4 — Rede Neural, Registry e Entrega

> **Fase:** 02 — Containers e Ambientes Reprodutíveis | **Etapa do TC:** 4

---

## 📋 Foco da Sessão

Modelo neural treinado para recomendação, registrado no MLflow Model Registry e documentado para entrega.

**Disciplina de referência:**
- [`04-dvc-mlflow`](../../04-dvc-mlflow/)

---

## 🎯 Objetivos

- Treinar MLP/embedding model com PyTorch para recomendação
- Comparar com baselines (Scikit-Learn) usando ≥ 4 métricas
- Registrar modelo no MLflow Model Registry (Staging → Production)
- Escrever Model Card com performance, limitações e viéses
- Preparar vídeo STAR e finalizar documentação

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Sistemas de recomendação: collaborative filtering vs. content-based
- Embeddings para representar usuários e itens
- MLflow Model Registry: ciclo de vida (None → Staging → Production)
- Model Card: por que documentar limitações?

### 2. Exercício Guiado (~40 min)

1. **Modelo de recomendação:**
   - Implementar MLP com embeddings (user_id, item_id → score)
   - Ou: MLP com features de interação tabulares
   - Training loop com PyTorch: DataLoader, optimizer, early stopping
2. **Comparação de modelos:**
   - Baseline 1: Popular items (frequency-based)
   - Baseline 2: SVD (Scikit-Learn/Surprise)
   - MLP PyTorch
   - Métricas: NDCG@K, Hit Rate@K, MAP, Recall@K
3. **Model Registry:**
   - `mlflow.pytorch.log_model(model, "recsys-model")`
   - Registrar no Model Registry
   - Promover: None → Staging → Production
   - Tag com versão e metadata
4. **Documentação final:**
   - Model Card: uso pretendido, métricas, limitações
   - README: setup completo, reproduzir do zero
   - Storyboard do vídeo STAR

### 3. Discussão Aberta (~20 min)

- Quando usar embeddings vs. features tabulares para recomendação?
- Como definir métricas de ranking (NDCG, MAP)?
- MLflow Model Registry vs. apenas salvar .pt: vantagens?
- Dicas para o vídeo STAR: estrutura e timing

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 4:** Repositório final + modelo no Registry + vídeo STAR

- [ ] MLP/embedding model funcional em PyTorch
- [ ] Comparação com ≥ 2 baselines usando ≥ 4 métricas
- [ ] Modelo registrado no MLflow Model Registry → Production
- [ ] Model Card completa
- [ ] README com instruções de setup + reprodução
- [ ] Vídeo STAR ≤ 5 min
- [ ] *(Opcional)* Deploy em nuvem via Docker

---

## 📚 Referências

- Material da disciplina: [`04-dvc-mlflow`](../../04-dvc-mlflow/)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)
- [PyTorch Embedding Layer](https://pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- Dataset sugerido: [Instacart Market Basket](https://www.kaggle.com/c/instacart-market-basket-analysis) ou [MovieLens](https://grouplens.org/datasets/movielens/)
