# Aula 03 — Pydantic: Validacao em Runtime

Pacote canonico para validar payloads de inferencia em runtime com uma
cadeia de validadores locais e um Strategy opcional usando Pydantic.

## Conceitos abordados

### Strategy Pattern

O **Strategy Pattern** permite trocar o backend de validacao sem alterar
o contrato da interface. Quando Pydantic esta disponivel, usamos; caso
contrario, um validador local deterministico entra em acao.

```
┌────────────┐     ┌──────────────────┐
│ Consumidor │────>│ SchemaStrategy   │ (Protocol)
└────────────┘     └──────────────────┘
                          ▲
                   ┌──────┴──────┐
                   │             │
            ┌──────────┐  ┌───────────┐
            │  Local   │  │ Pydantic  │
            └──────────┘  └───────────┘
```

### Chain of Responsibility

Validadores de **regras de negocio** sao compostos em cadeia. Cada handler
executa seu check e delega para o proximo:

1. **RequiredBusinessFields**: customer_id nao pode ser vazio
2. **NumericRange**: faixas operacionais do modelo (age 18-100)
3. **AllowedSegment**: segmentos aceitos pela politica de scoring
4. **Consistency**: regras cross-field (gasto zero + horizonte longo)

### Diferenca entre validacao de DataFrame e payload

| Aspecto | Pandera (Aula 02) | Pydantic (Aula 03) |
|---------|-------------------|---------------------|
| Granularidade | DataFrame inteiro | Registro individual |
| Caso de uso | Batch processing | APIs, serving |
| Tipo de dado | Tabular (colunas) | JSON/dict (campos) |

## Objetivo didatico

- Validar campos obrigatorios, faixas e tipos antes de processar inferencia.
- Separar schema validation de regras de negocio.
- Demonstrar Chain of Responsibility para compor validadores.
- Mostrar como proteger fronteiras de sistema.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula03-pydantic-runtime
python pydantic_validation.py
```

## Arquivos

- `pydantic_validation.py`: strategy opcional com Pydantic, cadeia de validadores
  de negocio e payloads de exemplo.
- `03_pydantic_runtime_local.ipynb`: notebook didatico com walkthrough interativo.

## Observacoes didaticas

- A cadeia facilita adicionar novos checks sem inflar uma unica funcao.
- Pydantic cobre schema e coercao, mas regras de negocio continuam explicitas.
- O mesmo padrao serve para APIs, jobs de scoring e workers assincronos.
- O ConsistencyHandler demonstra validacao cross-field, comum em producao.
