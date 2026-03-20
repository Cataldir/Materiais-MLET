# 02 — Fundamentos de Modelos de ML

> 6h de vídeo · 6 aulas

## Por que esta disciplina importa

Nenhuma trilha de ML Engineering se sustenta sem compreensão técnica dos modelos que serão treinados, comparados e operacionalizados. Esta disciplina organiza o repertório mínimo para que o estudante não trate algoritmos como caixas-pretas intercambiáveis, mas como escolhas com suposições, trade-offs e impactos práticos diferentes.

## O que você deve aprender

- revisar os fundamentos de splits, baselines e tipos de problema em ML;
- comparar modelos lineares, regularizados, ensembles e redes neurais em cenários distintos;
- interpretar métricas e estratégias de validação de forma tecnicamente correta;
- usar ferramentas de explicabilidade para entender comportamento de modelos;
- consolidar um fluxo end-to-end que una EDA, modelagem e documentação do resultado.

## Como usar este material

1. Use a aula introdutória para equalizar conceitos e convenções.
2. Avance pelas famílias de modelos comparando quando cada abordagem faz sentido.
3. Trate a aula de métricas e validação como eixo metodológico da disciplina.
4. Feche no projeto integrador para transformar comparação algorítmica em solução estruturada.

## Como referenciar esta disciplina no repositório

- O ponto de entrada oficial é a pasta `fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/`.
- Para citar conteúdo prático, aponte para a aula ou para a referência complementar mais adequada ao tema.
- As referências migradas desta disciplina funcionam como aprofundamento e ponte para lives e grupos de estudo.
- Use a governança canônica apenas quando a referência deixar de ser técnica e passar a ser acadêmica ou processual.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática profissional, essa disciplina melhora a qualidade das decisões de modelagem e reduz escolhas feitas por moda ou hábito. No plano acadêmico, ela reforça raciocínio comparativo, validade experimental e entendimento de limitações estatísticas, elementos essenciais para justificar tecnicamente um projeto de ML.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-intro-ml/) | Intro ML, Splits, baseline com Iris | `iris_intro_ml.py`, `01_intro_ml_iris.ipynb` |
| [02](aula02-regressao-regularizacao/) | Regressão Linear/Ridge/Lasso/Logística | `regularization_comparison.py` |
| [03](aula03-ensemble-shap/) | Árvore/RF/XGBoost/LightGBM + SHAP | `ensemble_comparison.py`, `shap_analysis.py` |
| [04](aula04-mlp-pytorch-keras/) | MLP PyTorch + Keras vs XGBoost | `mlp_pytorch.py`, `mlp_keras.py` |
| [05](aula05-metricas-validacao/) | Métricas avançadas e validação robusta | `metrics_toolkit.py` |
| [06](aula06-projeto-integrador/) | Projeto integrador end-to-end | notebook EDA→modelos→Model Card |

## Referências migradas

- [referencia-supervisionado-regressao-tuning](referencia-supervisionado-regressao-tuning/): regressão supervisionada, comparação de modelos e tuning com dataset público.
- [referencia-nao-supervisionado-clustering-pca](referencia-nao-supervisionado-clustering-pca/): clustering, silhouette, elbow e PCA como ponte para lives e grupos.
