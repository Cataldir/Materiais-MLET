# Aula 01 - Conceitos de cloud para ML

Pacote canonico leve para comparar tres padroes de inferencia sobre o mesmo modelo `scikit-learn`: lote, API em tempo real e invocacao estilo serverless.

## Objetivo didatico

- mostrar que o mesmo modelo pode ser servido com contratos operacionais diferentes;
- comparar latencia total, latencia media e throughput sem depender de conta cloud;
- usar apenas dataset publico embutido no `scikit-learn` e requests sintetizados localmente.

## O que foi preservado

- treinamento de um classificador tabular simples com `scikit-learn`;
- comparacao entre padroes classicos de deploy para ML;
- versoes em script e notebook com a mesma logica central.

## O que foi simplificado

- chamadas reais a servicos cloud, filas e gateways;
- credenciais, secrets e infraestrutura externa;
- qualquer dependencia alem de `numpy` e `scikit-learn`.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/01-deploy-em-nuvem/aula01-conceitos-cloud
python cloud_inference_patterns.py
```

## Arquivos

- `cloud_inference_patterns.py`: compara lote, API em tempo real e serverless para o mesmo modelo.
- `01_conceitos_cloud.ipynb`: notebook didatico com a mesma comparacao.

## Observacoes didaticas

- `batch` tende a ganhar em throughput quando varias requisicoes chegam juntas;
- `realtime_api` favorece simplicidade de contrato por request;
- `serverless` ajuda a explicar cold start e custo por invocacao sem depender de um provedor real.