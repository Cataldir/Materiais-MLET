# 📖 Grupo de Estudos 2 — Modelagem com Redes Neurais

> **Fase:** 01 — Produtização de Modelos | **Etapa do TC:** 2

---

## 📋 Foco da Sessão

Construção, treinamento e avaliação de MLP com PyTorch para classificação de churn.

**Disciplina de referência:**
- [`02-fundamentos-modelos-ml`](../../02-fundamentos-modelos-ml/)

---

## 🎯 Objetivos

- Construir MLP em PyTorch: arquitetura, função de ativação, loss function
- Implementar loop de treinamento com early stopping e batching
- Comparar MLP vs. baselines usando ≥ 4 métricas
- Analisar trade-off de custo (falso positivo vs. falso negativo)
- Registrar todos os experimentos no MLflow

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Anatomia de uma MLP: camadas, neurônios, ativações
- Funções de perda para classificação binária (BCELoss, CrossEntropyLoss)
- O que é early stopping e por que usamos?
- Diferença entre batch, mini-batch e SGD

### 2. Exercício Guiado (~40 min)

1. **Definir arquitetura MLP:**
   - Input: número de features do dataset
   - Hidden layers: 2-3 camadas com ReLU
   - Output: 1 neurônio + Sigmoid (ou 2 + Softmax)
2. **Implementar training loop:**
   - DataLoader com batch_size=64
   - Adam optimizer, lr=1e-3
   - Early stopping com patience=10
3. **Comparar modelos:**
   - Tabela: Accuracy, Precision, Recall, F1, AUC-ROC
   - MLP vs. LogisticRegression vs. RandomForest vs. XGBoost
4. **Análise de custo:**
   - Definir custo de FP (ação desnecessária) vs. FN (perder cliente)
   - Ajustar threshold de decisão com base no custo

### 3. Discussão Aberta (~20 min)

- Quando uma MLP é melhor que modelos tabulares clássicos?
- Como decidir o número de camadas e neurônios?
- Overfitting: como diagnosticar e mitigar?
- Vale a pena tentar ensemble (MLP + XGBoost)?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 2:** Tabela comparativa de modelos + MLP treinado + artefatos no MLflow

- [ ] MLP funcional em PyTorch com early stopping
- [ ] Comparação com ≥ 3 baselines usando ≥ 4 métricas
- [ ] Análise de trade-off de custo documentada
- [ ] Todos os experimentos registrados no MLflow
- [ ] Melhor modelo identificado e justificado

---

## 📚 Referências

- Material da disciplina: [`02-fundamentos-modelos-ml`](../../02-fundamentos-modelos-ml/)
- [PyTorch Tutorials — Neural Networks](https://pytorch.org/tutorials/beginner/blitz/neural_networks_tutorial.html)
- [MLflow Model Registry](https://mlflow.org/docs/latest/model-registry.html)

## Artefatos de acompanhamento

- [Guia de estudo](guia-de-estudo.md)
- [Atividade do aluno](atividade-do-aluno.md)
- [Checklist tech challenge](checklist-tech-challenge.md)
- [Script Python de apoio](apoio_estudo.py)
