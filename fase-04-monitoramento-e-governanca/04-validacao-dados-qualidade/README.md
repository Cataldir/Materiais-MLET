# 04 — Validacao de Dados e Bibliotecas de Qualidade

> 4h de video · 4 aulas + solucao end-to-end

## Por que esta disciplina importa

Muitos incidentes de ML nao surgem no modelo, mas na entrada errada que o
sistema aceita sem contestar. Esta disciplina mostra como validar dados, contratos e
qualidade operacional antes que o problema se propague para treino, serving ou
monitoramento tardio.

## O que voce deve aprender

- Usar Great Expectations para suites e checkpoints de qualidade.
- Definir schemas tipados com Pandera.
- Validar payloads e estruturas em runtime com Pydantic.
- Incorporar gates de qualidade em pipelines executaveis.
- Integrar todos os pilares em uma pipeline end-to-end.

## Conceitos fundamentais

### Validacao declarativa vs. imperativa

| Abordagem | Exemplo | Quando usar |
|-----------|---------|-------------|
| **Imperativa** | `assert df['age'].min() >= 0` | Scripts rapidos, POCs |
| **Declarativa** | `ExpectationSpec("age_min", "age", MIN, 0)` | Pipelines de producao |

A abordagem declarativa separa **o que validar** de **como executar**, permitindo
reutilizar regras em ambientes diferentes e documentar contratos automaticamente.

### Camadas de validacao em ML

```
┌─────────────────────────────────────────────────────┐
│                  Quality Gate (Aula 04)              │
│         Decisao final: pass / warn / fail            │
├─────────────────────────────────────────────────────┤
│              Runtime Validation (Aula 03)            │
│     Pydantic + Chain of Responsibility               │
│     Protege fronteiras: APIs, workers, serving       │
├─────────────────────────────────────────────────────┤
│              Schema Validation (Aula 02)             │
│     Pandera — contratos tipados para DataFrames      │
│     Valida entrada e saida do modelo                 │
├─────────────────────────────────────────────────────┤
│           Expectation Suite (Aula 01)                │
│     Great Expectations — regras declarativas         │
│     Completude, faixa, cardinalidade, unicidade      │
└─────────────────────────────────────────────────────┘
```

## Como usar este material

1. Comece pela **Aula 01** para entender expectativas declarativas.
2. Avance para **Aula 02** para schemas tipados em DataFrames.
3. Na **Aula 03**, aprenda validacao de registros individuais (payloads).
4. Na **Aula 04**, combine tudo em gates de qualidade com decisao.
5. Execute a **solucao end-to-end** para ver a integracao completa.

## Aulas

| Aula | Tema | Artefatos |
|------|------|-----------|
| 01 | Great Expectations: suites + checkpoints | `ge_validation.py`, notebook |
| 02 | Pandera: DataFrameSchema tipada | `pandera_schemas.py`, notebook |
| 03 | Pydantic + Chain of Responsibility | `pydantic_validation.py`, notebook |
| 04 | Pipeline com gates de qualidade | `quality_gates.py`, notebook |
| E2E | Integracao end-to-end | `e2e_validation_pipeline.py`, notebook |

## Execucao rapida

```bash
# Aula individual
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula01-great-expectations
python ge_validation.py

# Solucao end-to-end
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade
python e2e_validation_pipeline.py
```

## Referenciais teoricos da disciplina

Consulte o indice local em [referencias/README.md](referencias/README.md) para
leituras e documentacao de apoio.

## Relevancia para a pratica executiva e academica

Em operacoes reais, validacao de dados reduz custo de incidente e eleva
confianca em pipelines. Academicamente, a disciplina ajuda a formalizar qualidade de
entrada e consistencia de artefatos, aproximando engenharia de ML de praticas mais
robustas de especificacao e verificacao.
