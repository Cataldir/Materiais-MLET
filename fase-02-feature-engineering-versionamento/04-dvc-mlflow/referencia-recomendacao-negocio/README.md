# Referência Canônica — Caso de Negócio para Recomendação

Pacote derivado de `origin/recommendation-systems`, consolidando três ideias reutilizáveis da branch original:

- baseline por popularidade;
- engenharia de features orientada a negócio;
- modelagem de propensão para priorização comercial.

## Normalização aplicada

- remoção de dependências em `.env`, Azure OpenAI e binários locais;
- consolidação em um único script com dataset sintético reproduzível;
- notebook de apoio para exploração rápida em sala.

## Execução

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/referencia-recomendacao-negocio
python business_case_recommendation.py
```

## Arquivos

- `business_case_recommendation.py`: geração do cenário, features, baseline e ranking por propensão.
- `01_recomendacao_negocio.ipynb`: versão notebook para exploração guiada.

## Objetivo pedagógico

Este material encaixa a branch legada em uma trilha de fase 02: a turma trabalha um caso comercial, transforma eventos em features reutilizáveis e compara um baseline simples com um score supervisionado.