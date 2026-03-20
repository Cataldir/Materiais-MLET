# Referencia Canonica - NLP Preprocessamento e Sentimento

Pacote derivado de `origin/nlp-lectures`, consolidando os elementos mais reutilizaveis de preprocessamento textual e classificacao de sentimento em uma forma leve para a fase 05.

## O que foi preservado

- foco em limpeza de texto para portugues;
- framing binario de sentimento a partir de notas;
- paridade entre script executavel e notebook didatico;
- opcao de usar um CSV publico sem credenciais.

## O que foi removido

- Docker, devcontainer e setup acoplado ao ambiente da branch legada;
- downloads obrigatorios de NLTK e outros pacotes pesados;
- Optuna, serializacao de modelos e artefatos de experimento;
- dependencias de dados locais grandes.

## Execucao

```bash
cd fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/referencia-nlp-preprocessamento-sentimento
python text_preprocessing_and_sentiment.py
```

Para testar com a fonte publica inspirada no material legado:

```bash
python text_preprocessing_and_sentiment.py --public-dataset --max-rows 300
```

## Arquivos

- `text_preprocessing_and_sentiment.py`: preprocessador leve e baseline Naive Bayes com dataset embutido por padrao.
- `01_preprocessamento_sentimento.ipynb`: notebook com o mesmo fluxo principal para demonstracao em aula.

## Observacoes didaticas

- este pack serve como referencia de NLP classico antes de comparar com pipelines de LLMs e agentes;
- a execucao padrao nao usa variaveis de ambiente nem downloads manuais;
- a rota `--public-dataset` e opcional e usa um CSV aberto na internet, mantendo o baseline local como caminho principal.