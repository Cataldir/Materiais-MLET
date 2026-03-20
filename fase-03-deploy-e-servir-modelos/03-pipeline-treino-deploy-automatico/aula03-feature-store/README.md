# Aula 03 - Feature store local

Pacote canonico local para simular um feature store com leitura point-in-time. O foco e mostrar como evitar leakage temporal no treino sem depender de um servico externo.

## Objetivo didatico

- registrar features por entidade e instante de observacao;
- materializar linhas de treino com leitura point-in-time;
- introduzir a ideia de repositorio local de features reutilizaveis.

## O que foi preservado

- separacao entre grupos de features;
- consulta temporal sem usar informacao futura;
- visao de registry e de dataset de treino.

## O que foi simplificado

- sem banco online/offline e sem servico de baixa latencia;
- sem store distribuido ou atualizacao em streaming;
- tudo fica em memoria com biblioteca padrao.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/aula03-feature-store
python feature_store_simulation.py
```

## Arquivos

- `feature_store_simulation.py`: registry local com consulta point-in-time para treino.

## Observacoes didaticas

- leakage temporal costuma aparecer quando a feature mais nova e usada fora do recorte;
- repositorio local ajuda a explicar o papel de versionamento e governanca de features;
- o mesmo padrao pode evoluir para store online e offline mais tarde.