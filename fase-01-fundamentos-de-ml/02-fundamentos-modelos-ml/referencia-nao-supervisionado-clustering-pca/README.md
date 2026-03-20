# Referencia Canonica - Clustering e PCA

Pacote canonico derivado do ZIP legado `ApremdizadoNaoSupervisionado`, com foco em clustering, elbow, silhouette e PCA.

## O que foi preservado

- narrativa de descoberta de grupos sem target supervisionado;
- comparacao de valores de `k` com metricas simples de qualidade;
- projecao em PCA para visualizacao e interpretacao inicial.

## O que foi removido

- notebooks longos com multiplas demos desconectadas;
- datasets locais grandes e caminhos fixos do legado;
- tecnicas mais especializadas que exigiriam contexto adicional para esta fase.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/02-fundamentos-modelos-ml/referencia-nao-supervisionado-clustering-pca
python unsupervised_clustering_pca.py
```

## Arquivos

- `unsupervised_clustering_pca.py`: demo com busca simples de `k`, silhouette, inertia e PCA em 2 componentes.
- `01_clustering_pca_wine.ipynb`: notebook enxuto com a mesma logica principal.

## Observacoes didaticas

- este material entra como referencia de enriquecimento para lives e grupos de estudo, sem virar uma trilha paralela ao curriculo principal;
- o dataset vem do `scikit-learn`, o que preserva a execucao local e publica.