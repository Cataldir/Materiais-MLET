# Referência Canônica — MLflow para Sumarização

Pacote derivado de `origin/mlflow-bentoml/summarization`, normalizado para a árvore canônica da fase 02.

## O que foi preservado

- rastreamento explícito de parâmetros, métricas e artefatos no MLflow;
- logging de um modelo `pyfunc` com assinatura inferida;
- caso educacional de sumarização textual com execução local e sem credenciais.

## O que foi removido

- dependência de modelos externos do Hugging Face;
- tags de usuário específicas da branch de origem;
- acoplamento com estrutura `requirements/` da branch legada.

## Execução

```bash
cd fase-02-feature-engineering-versionamento/04-dvc-mlflow/referencia-mlflow-sumarizacao
python text_summarization_tracking.py
```

O script cria um diretório local `mlruns/` dentro desta pasta e registra um baseline de sumarização rule-based. Isso mantém um caminho público e reproduzível por padrão, sem depender de variáveis de ambiente.

## Arquivos

- `text_summarization_tracking.py`: experimento canônico, com dataset embutido e modelo `mlflow.pyfunc`.

## Observações didáticas

- o objetivo aqui é ensinar tracking e empacotamento de modelo, não qualidade state-of-the-art de NLP;
- o baseline rule-based substitui o modelo original da branch porque checkpoints e pesos não fazem parte da baseline pública.