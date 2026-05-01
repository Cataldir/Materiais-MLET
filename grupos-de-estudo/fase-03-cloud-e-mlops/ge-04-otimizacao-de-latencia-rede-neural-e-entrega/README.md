# 📖 Grupo de Estudos 4 — Otimização de Latência, Rede Neural e Entrega

> **Fase:** 03 — Cloud e MLOps | **Etapa do TC:** 4

---

## 📋 Foco da Sessão

Modelo neural otimizado para produção com técnicas de redução de latência e entrega final.

**Disciplina de referência:**
- [`06-latencia-performance`](../../../fase-03-cloud-e-mlops/06-latencia-performance/)

---

## 🎯 Objetivos

- Treinar DistilBERT/MLP com PyTorch Lightning para classificação de triagem
- Aplicar ≥ 1 otimização: quantização INT8, ONNX Runtime ou pruning
- Criar benchmark pós-otimização com curva Pareto (latência × acurácia)
- Registrar modelo otimizado no MLflow Model Registry → Production
- Finalizar Model Card, README e vídeo STAR

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Técnicas de otimização de latência em NLP:
  - Quantização: FP32 → INT8 (redução de 2-4x em latência)
  - ONNX Runtime: graph optimizations, operator fusion
  - Pruning: remover pesos menos importantes
  - Distilação: modelo menor que aprende do maior
- Trade-off Pareto: latência vs. acurácia
- PyTorch Lightning: organização de código de treino

### 2. Exercício Guiado (~40 min)

1. **Treinar DistilBERT com Lightning:**
   - `LightningModule` com `training_step`, `validation_step`
   - Callbacks: `EarlyStopping`, `ModelCheckpoint`
   - Logger: MLflow
2. **Quantização INT8:**
   ```python
   import torch.quantization
   quantized_model = torch.quantization.quantize_dynamic(
       model, {torch.nn.Linear}, dtype=torch.qint8
   )
   ```
   - Medir latência antes/depois
3. **ONNX Export:**
   ```python
   torch.onnx.export(model, dummy_input, "model.onnx")
   # Inferência com ONNX Runtime
   import onnxruntime as ort
   session = ort.InferenceSession("model.onnx")
   ```
4. **Curva Pareto:**
   - Tabela: Original, Quantized, ONNX, Quantized+ONNX
   - Métricas: Latência P50, P95, Throughput, F1, AUC-ROC
   - Gráfico: latência no eixo X, acurácia no eixo Y
5. **Registrar melhor modelo:**
   - Escolher ponto Pareto que atende SLO (P95 < 200 ms)
   - `mlflow.register_model()` → Production

### 3. Discussão Aberta (~20 min)

- Quantização: quando a perda de acurácia é aceitável?
- ONNX vs. TorchScript vs. TensorRT: qual usar quando?
- Como convencer stakeholders que "2% menos de F1" vale "3x mais rápido"?
- PyTorch Lightning vs. plain PyTorch: overhead justificado?

### 4. Conexão com Tech Challenge (~10 min)

**Entregável da Etapa 4:** Modelo otimizado + curva Pareto + Model Card + vídeo STAR

- [ ] DistilBERT/MLP treinado com PyTorch Lightning
- [ ] ≥ 1 otimização aplicada (quantização, ONNX ou pruning)
- [ ] Benchmark com curva Pareto (latência × acurácia)
- [ ] SLO P95 < 200 ms atingido (ou documentar por que não)
- [ ] Modelo registrado no MLflow Registry → Production
- [ ] Model Card completa
- [ ] Vídeo STAR ≤ 5 min

---

## 📚 Referências

- Material da disciplina: [`06-latencia-performance`](../../../fase-03-cloud-e-mlops/06-latencia-performance/)
- [ONNX Runtime](https://onnxruntime.ai/)
- [PyTorch Quantization](https://pytorch.org/docs/stable/quantization.html)
- [PyTorch Lightning Docs](https://lightning.ai/docs/pytorch/stable/)
