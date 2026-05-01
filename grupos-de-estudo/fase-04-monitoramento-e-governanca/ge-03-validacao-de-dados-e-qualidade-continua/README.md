# 📖 Grupo de Estudos 3 — Validação de Dados e Qualidade Contínua

> **Fase:** 04 — Monitoramento e Governança | **Etapa do TC:** 3

---

## 📋 Foco da Sessão

Validação automatizada de dados com profiling, deduplicação, data contracts e quality gates.

**Disciplinas de referência:**
- [`04-validacao-dados`](../../../fase-04-monitoramento-e-governanca/04-validacao-dados/)
- [`03-monitoramento-pipelines`](../../../fase-04-monitoramento-e-governanca/03-monitoramento-pipelines/)

---

## 🎯 Objetivos

- Executar profiling automatizado com ydata-profiling (≥ 4 dimensões)
- Implementar deduplicação: hash (exatas) + fuzzy matching (aproximadas)
- Criar data contracts com Pandera (DataFrameModel)
- Construir validation suite com Great Expectations (≥ 10 expectations)
- Implementar pipeline fail-fast: abortar se contract violado
- Detectar outliers com ≥ 1 método

---

## 🗂️ Roteiro de Discussão

### 1. Revisão Conceitual (~20 min)

- Dimensões de qualidade de dados: completude, unicidade, consistência, validade
- Data contracts: o que são e por que importam em pipelines de ML?
- Pandera vs. Great Expectations: abordagens complementares
- Fail-fast principle: detectar problemas cedo no pipeline

### 2. Exercício Guiado (~40 min)

1. **Profiling:**
   ```python
   from ydata_profiling import ProfileReport
   profile = ProfileReport(df, title="Credit Data Quality Report")
   profile.to_file("quality_report.html")
   ```
   - Analisar: missing values, correlações, distribuições, duplicatas

2. **Deduplicação:**
   - Hash-based: `df.drop_duplicates()` para exatas
   - Fuzzy: `thefuzz` para campos de texto (nome, endereço)
   - Reportar: quantas duplicatas encontradas por método

3. **Data contracts (Pandera):**
   ```python
   import pandera as pa
   
   class CreditSchema(pa.DataFrameModel):
       age: int = pa.Field(ge=18, le=100)
       income: float = pa.Field(ge=0)
       loan_amount: float = pa.Field(ge=0)
       employment_years: int = pa.Field(ge=0)
       
       class Config:
           strict = True
   ```
   - Integrar no pipeline antes do treinamento

4. **Great Expectations:**
   - Suite com ≥ 10 expectations: not_null, unique, between, regex, etc.
   - Checkpoint que roda automaticamente
   - Gerar Data Docs (HTML report)

5. **Pipeline fail-fast:**
   - Se Pandera schema falha → `raise DataContractViolation(...)`
   - Log estruturado com detalhes da violação
   - Pipeline aborta antes de atingir o modelo

### 3. Discussão Aberta (~20 min)

- Validação rígida (fail) vs. soft (warn): quando usar cada abordagem?
- Como lidar com schema evolution (novas features, tipos alterados)?
- Custo de validação: quanto overhead é aceitável no pipeline?
- Great Expectations em produção: quem mantém as expectations atualizadas?

### 4. Conexão com Tech Challenge (~10 min)

**Critérios de aceite da Etapa 3:**

- [ ] Profiling com 4+ dimensões gerado automaticamente
- [ ] Deduplicação aplicada (hash + fuzzy)
- [ ] Data contract Pandera integrado ao pipeline
- [ ] Validation suite GE com ≥ 10 expectations
- [ ] Pipeline aborta se contract é violado
- [ ] ≥ 1 método de detecção de outliers implementado

---

## 📚 Referências

- Material das disciplinas: [`04-validacao-dados`](../../../fase-04-monitoramento-e-governanca/04-validacao-dados/), [`03-monitoramento-pipelines`](../../../fase-04-monitoramento-e-governanca/03-monitoramento-pipelines/)
- [Pandera Documentation](https://pandera.readthedocs.io/)
- [Great Expectations Docs](https://docs.greatexpectations.io/)
- [ydata-profiling](https://docs.profiling.ydata.ai/)
