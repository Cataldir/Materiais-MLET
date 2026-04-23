# Aula 02 — Pandera: Contratos Tipados de DataFrame

Pacote canonico para validacao de dados com Pandera em um pipeline local de ML.
O material continua funcional mesmo quando a biblioteca nao esta instalada.

## Conceitos abordados

### DataFrameSchema

Um schema Pandera define o **contrato tipado** de um DataFrame: quais colunas
existem, seus tipos, restricoes de faixa e regras cross-column.

```python
pa.DataFrameSchema(
    columns={
        "tenure": pa.Column(int, checks=[pa.Check.greater_than_or_equal_to(0)]),
        "churn": pa.Column(str, checks=[pa.Check.isin(["yes", "no"])]),
    }
)
```

### Schema de entrada vs. schema de saida

Em ML, validamos **tanto a entrada quanto a saida** do modelo:

| Schema | O que valida | Quando aplicar |
|--------|-------------|----------------|
| **Entrada** | Dados brutos antes de transformacao | Ingestao, feature engineering |
| **Saida** | Predicoes do modelo | Pos-inferencia, serving |

### Validacao lazy

Pandera pode acumular **todos os erros** antes de levantar excecao,
em vez de parar no primeiro. Isso facilita diagnostico:

```python
schema.validate(df, lazy=True)  # Acumula erros
```

### Coercao de tipos

Pandera pode converter tipos automaticamente (`coerce=True`), o que e
util quando dados chegam como strings de um CSV ou API.

## Objetivo didatico

- Definir schemas tipados para dados de entrada e predicoes.
- Comparar exemplos validos e invalidos com a mesma estrutura.
- Demonstrar fallback amigavel quando `pandera` nao esta disponivel.
- Mostrar a diferenca entre validar entrada e saida do modelo.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula02-pandera
python pandera_schemas.py
```

## Arquivos

- `pandera_schemas.py`: schemas de entrada (churn, titanic) e saida (predicoes),
  datasets sinteticos e motor de validacao.
- `02_pandera_local.ipynb`: notebook didatico com os mesmos exemplos.

## Observacoes didaticas

- `pandera[pandas]` e a instalacao recomendada para o backend `pandas`.
- Quando a dependencia nao existe, o script registra aviso e retorna resultados
  indicando que o backend nao esta disponivel.
- Schemas de saida sao tao importantes quanto schemas de entrada em producao.
