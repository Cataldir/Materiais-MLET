# Aula 01 — Great Expectations: Suites e Checkpoints

Pacote canonico para introduzir suites de expectativa e checkpoints sem
exigir instalacao obrigatoria do Great Expectations. O script usa um fallback
local que implementa a mesma semantica.

## Conceitos abordados

### Expectativa declarativa

Uma expectativa e uma **regra expressa como especificacao**, nao como codigo
imperativo. Em vez de escrever `assert df['age'].min() >= 0`, declaramos:

```python
ExpectationSpec("age_min", "age", ExpectationKind.MIN, 0.0)
```

Isso separa **o que validar** de **como executar**.

### Suite de expectativas

Uma suite agrupa expectativas em um contrato testavel. A suite e o equivalente
a um contrato de qualidade: define todas as regras que um dataset deve satisfazer.

### Checkpoint

Um checkpoint executa uma suite sobre um dataset e consolida o resultado em
aprovado ou reprovado, com detalhes por expectativa.

### Tipos de expectativas implementados

| Tipo | Descricao | Exemplo |
|------|-----------|---------|
| `MIN` | Valor minimo da coluna | tenure >= 0 |
| `MAX` | Valor maximo da coluna | tenure <= 120 |
| `BETWEEN` | Faixa de valores | monthly_charges entre 0 e 500 |
| `SET` | Valores permitidos | contract in {month-to-month, one_year, two_year} |
| `MISSING` | Taxa maxima de nulos | <= 5% de nulos em monthly_charges |
| `UNIQUE` | Sem duplicatas | customer_id unico |
| `NOT_NULL` | Nenhum nulo | tenure preenchido |

## Objetivo didatico

- Mostrar o formato mental de expectativas declarativas para qualidade de dados.
- Separar a definicao das regras da execucao do checkpoint.
- Manter um contrato testavel que funcione em qualquer ambiente local.
- Demonstrar export de resultados como JSON para integracao com CI/CD.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/04-validacao-dados-qualidade/aula01-great-expectations
python ge_validation.py
```

## Arquivos

- `ge_validation.py`: motor de expectativas, suites (Titanic e Churn), checkpoint e relatorios.
- `01_great_expectations_local.ipynb`: notebook didatico com walkthrough interativo.

## Observacoes didaticas

- O material destaca o conceito de expectation suite antes da ferramenta em si.
- A mesma declaracao pode ser expandida para pipelines maiores com GX completo.
- O fallback local facilita smoke tests e ambientes de estudo mais leves.
- Resultados podem ser exportados como JSON para integracao com sistemas externos.
