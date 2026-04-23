# Aula 04 — Pipeline com Gates de Qualidade

Pacote canonico para demonstrar como um pipeline de dados pode bloquear ou
liberar lotes com uma decisao `pass`, `warn` ou `fail`.

## Conceitos abordados

### Quality Gate

Um quality gate e um **ponto de decisao** em uma pipeline que determina se
um lote de dados pode prosseguir ou deve ser bloqueado.

```
Lote de dados → [Missing] → [Duplicatas] → [Faixa] → [Schema] → Decisao
                                                                    │
                                                        ┌───────────┼───────────┐
                                                        │           │           │
                                                      PASS        WARN        FAIL
                                                    (segue)   (ressalvas)  (bloqueado)
```

### Tres estados de decisao

| Estado | Significado | Acao |
|--------|-------------|------|
| **pass** | Lote limpo, pronto para seguir | Prosseguir na pipeline |
| **warn** | Problemas menores detectados | Prosseguir com alerta operacional |
| **fail** | Problemas criticos detectados | Bloquear antes de treino/serving |

### Thresholds configuraveis

Cada check tem dois limites: `warn` e `fail`. Valores abaixo de `warn` sao
aceitos; entre `warn` e `fail` geram aviso; acima de `fail` bloqueiam.

```python
GateThresholds(
    missing_warn=0.03,   # 3% de nulos → aviso
    missing_fail=0.10,   # 10% de nulos → bloqueio
)
```

### Template Method

A pipeline segue uma sequencia fixa (Template Method):
1. **Gerar** lotes de dados
2. **Validar** com checks individuais
3. **Decidir** com base nos resultados
4. **Resumir** em relatorio

## Objetivo didatico

- Transformar checks de qualidade em contrato objetivo para a esteira.
- Combinar missing values, duplicidade e violacoes de faixa em decisao unica.
- Mostrar diferenca entre lote aceito com observacao e lote bloqueado.
- Demonstrar export de resultados como JSON para CI/CD.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula04-pipeline-gates
python quality_gates.py
```

## Arquivos

- `quality_gates.py`: datasets sinteticos, checks de qualidade, motor de decisao
  e relatorios em texto e JSON.
- `04_pipeline_gates_local.ipynb`: notebook com a mesma sequencia para exploracao.

## Observacoes didaticas

- `pass` indica lote pronto para seguir a esteira.
- `warn` indica lote liberado com ressalvas e observacao operacional.
- `fail` indica bloqueio do lote antes de treino, scoring ou publicacao de artefato.
- Thresholds sao configuraveis e devem ser calibrados por dominio.
