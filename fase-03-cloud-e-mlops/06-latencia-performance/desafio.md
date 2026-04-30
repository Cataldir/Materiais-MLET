# Desafio — Latência e Performance em Dados Não Estruturados

> **Tipo:** Individual · Não obrigatório · Sem nota  
> **Limite:** 2 páginas (≈ 1 000 palavras)

---

## 1. Contexto

Uma empresa de mídia precisa servir um modelo de classificação de texto (BERT) com latência < 100 ms por request. O modelo atual roda em CPU e tem P95 de 350 ms. O aluno deve aplicar técnicas de **compressão e otimização** para atingir o SLO sem degradar significativamente a acurácia.

## 2. Objetivos de Aprendizagem

| # | Objetivo |
|---|----------|
| O1 | Comparar BERT vs. DistilBERT em latência e acurácia. |
| O2 | Aplicar quantização pós-treino (INT8) e medir impacto. |
| O3 | Converter modelo para ONNX Runtime e benchmarkar. |
| O4 | Traçar curva Pareto (latência × acurácia) das variantes. |

## 3. Escopo e Limites

- **Inclui:** Benchmark, compressão (quantização, distilação), conversão ONNX, Pareto.
- **Exclui:** GPU/TPU (coberto na aula, não é foco do desafio); inferência distribuída.

## 4. Requisitos

### Funcionais (RF)
| RF | Descrição |
|----|-----------|
| RF-01 | Benchmark de ≥ 3 variantes do modelo (original, distilled, quantized). |
| RF-02 | Conversão para ONNX com medição de speedup. |
| RF-03 | Curva Pareto: latência (P95) × acurácia para todas as variantes. |

### Não Funcionais (RNF)
| RNF | Descrição |
|-----|-----------|
| RNF-01 | Todos os testes em CPU (comparabilidade). |
| RNF-02 | Dataset de classificação com ≥ 1 000 amostras para benchmark. |

## 5. Passo a Passo (4 etapas)

| Etapa | Ação | Referência |
|-------|------|-----------|
| 1 | Servir BERT original e medir baseline (P50, P95, acurácia). | Aula 01–02 |
| 2 | Substituir por DistilBERT e re-benchmark. | Aula 02 |
| 3 | Quantizar (INT8) e converter para ONNX Runtime. | Aulas 04, 06 |
| 4 | Traçar curva Pareto e recomendar variante para o SLO. | Aula 04 |

## 6. Entregáveis

| # | Artefato | Formato |
|---|---------|---------|
| E1 | Relatório de benchmark com tabela comparativa | Markdown |
| E2 | Script de benchmark | Python (`.py`) |
| E3 | Gráfico Pareto (latência × acurácia) | PNG ou SVG |

## 7. Checklist de Validação

- [ ] Baseline medido: P50, P95, acurácia do modelo original.
- [ ] ≥ 3 variantes benchmarkadas.
- [ ] Conversão ONNX realizada com speedup documentado.
- [ ] Quantização INT8 aplicada com degradação de acurácia medida.
- [ ] Curva Pareto gerada com recomendação final.

## 8. Rubrica de Auto-Avaliação

| Critério | ⭐ Básico | ⭐⭐ Intermediário | ⭐⭐⭐ Avançado |
|----------|----------|-------------------|---------------|
| Variantes | 2 variantes | 3 variantes com métricas | 4+ variantes + ONNX + quantized |
| Benchmark | Latência média | P50 + P95 | P50 + P95 + P99 + throughput |
| Análise | Tabela comparativa | Pareto 2D | Pareto + recomendação + trade-offs |

## 9. Matriz de Rastreabilidade

| Objetivo | Requisito | Etapa | Entregável | Aulas |
|----------|-----------|-------|------------|-------|
| O1 | RF-01 | 1–2 | E1 | Aulas 01–02 |
| O2 | RF-01 | 3 | E1 | Aula 04 |
| O3 | RF-02 | 3 | E2 | Aula 06 |
| O4 | RF-03 | 4 | E3 | Aula 04 |

## 10. Extensões Opcionais

- Aplicar pruning e medir impacto adicional (Aula 04).
- Fine-tune com LoRA e comparar vs. full fine-tune (Aula 05).
- Testar com GPU e medir speedup adicional (Aula 06).

## 11. Checklist Rápido

- [ ] Li as aulas 01–08.
- [ ] Medi baseline do modelo original.
- [ ] Testei DistilBERT + quantização + ONNX.
- [ ] Tracei curva Pareto.
- [ ] Recomendei variante para o SLO.
- [ ] Documento ≤ 2 páginas.
