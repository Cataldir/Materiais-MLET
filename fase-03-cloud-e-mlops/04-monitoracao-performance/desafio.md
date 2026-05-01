# Desafio — Monitoração de Performance

> **Tipo:** Individual · Não obrigatório · Sem nota  
> **Limite:** 2 páginas (≈ 1 000 palavras)

---

## 1. Contexto

Uma adtech serve um modelo de recomendação de anúncios com SLA de **P99 < 150 ms**. Nos últimos meses, a latência subiu e o throughput caiu, mas o time não consegue identificar o gargalo. O aluno deve conduzir um **diagnóstico de performance** e propor otimizações.

## 2. Objetivos de Aprendizagem

| # | Objetivo |
|---|----------|
| O1 | Medir latência (P50, P95, P99) e throughput de endpoint de inferência. |
| O2 | Identificar gargalos via profiling (preprocess, predict, postprocess). |
| O3 | Aplicar ≥ 2 técnicas de otimização (quantização, ONNX, batching, caching). |
| O4 | Definir SLOs e configurar alertas. |

## 3. Escopo e Limites

- **Inclui:** Benchmark, profiling, otimização e definição de SLOs.
- **Exclui:** Deploy em nuvem; configuração de Grafana (coberto na disciplina 05).

## 4. Requisitos

### Funcionais (RF)
| RF | Descrição |
|----|-----------|
| RF-01 | Relatório de benchmark com P50, P95, P99 antes e depois das otimizações. |
| RF-02 | Profile de inferência mostrando tempo gasto em cada etapa. |
| RF-03 | ≥ 2 otimizações aplicadas com medição de ganho. |

### Não Funcionais (RNF)
| RNF | Descrição |
|-----|-----------|
| RNF-01 | Usar locust ou k6 para benchmark. |
| RNF-02 | Modelo pode ser sklearn, PyTorch ou ONNX. |

## 5. Passo a Passo (4 etapas)

| Etapa | Ação | Referência |
|-------|------|-----------|
| 1 | Servir modelo via FastAPI e medir baseline (P50, P95, P99, throughput). | Aula 01 |
| 2 | Profiling do endpoint: medir tempo de cada etapa. | Aula 02 |
| 3 | Aplicar otimizações: ONNX Runtime, quantização, batch inference, caching. | Aulas 02–04 |
| 4 | Re-benchmark e definir SLOs formais. | Aula 01, Aula 08 |

## 6. Entregáveis

| # | Artefato | Formato |
|---|---------|---------|
| E1 | Relatório de benchmark (antes/depois) | Markdown |
| E2 | Script de profiling | Python (`.py`) |
| E3 | Documento de SLOs | Tabela no relatório |

## 7. Checklist de Validação

- [ ] Baseline medido: P50, P95, P99, requests/s.
- [ ] Profile com tempos de preprocess, predict, postprocess.
- [ ] ≥ 2 otimizações aplicadas (ex.: ONNX + caching).
- [ ] Benchmark pós-otimização mostrando ganho.
- [ ] SLOs definidos com thresholds claros.

## 8. Rubrica de Auto-Avaliação

| Critério | ⭐ Básico | ⭐⭐ Intermediário | ⭐⭐⭐ Avançado |
|----------|----------|-------------------|---------------|
| Benchmark | Tempo médio apenas | P50 + P95 | P50 + P95 + P99 + throughput |
| Profiling | Tempo total | 2 etapas medidas | 3+ etapas + gráfico |
| Otimização | 1 técnica | 2 técnicas com medição | 3+ técnicas + Pareto |

## 9. Matriz de Rastreabilidade

| Objetivo | Requisito | Etapa | Entregável | Aulas |
|----------|-----------|-------|------------|-------|
| O1 | RF-01 | 1 | E1 | Aula 01 |
| O2 | RF-02 | 2 | E2 | Aula 02 |
| O3 | RF-03 | 3 | E1 | Aulas 02–04 |
| O4 | — | 4 | E3 | Aula 08 |

## 10. Extensões Opcionais

- Comparar pipelines batch vs. real-time para o mesmo modelo (Aula 05).
- Testar aceleração GPU vs. CPU para modelo PyTorch (Aula 06).

## 11. Checklist Rápido

- [ ] Li as aulas 01–08.
- [ ] Servi modelo e medi baseline.
- [ ] Fiz profiling das etapas.
- [ ] Apliquei ≥ 2 otimizações.
- [ ] Re-benchmark com ganho documentado.
- [ ] Documento ≤ 2 páginas.
