# Referência Canônica — Productization de Modelo Sequencial

Pacote derivado do diretório `productization/` em `origin/deep-learning`, reduzido para uma baseline pública de deploy e monitoramento.

## O que foi preservado

- estrutura de API com health check, inferência e avaliação de qualidade;
- separação explícita entre lógica de qualidade e camada HTTP;
- foco em readiness operacional para um modelo sequencial.

## O que foi excluído

- `mlruns/`, checkpoints `.ckpt`, pesos `.pt` e artefatos de treinamento;
- Terraform e empacotamento de infraestrutura;
- dependência em diretórios locais ocultos e caminhos específicos de máquina.

## Execução

```bash
cd fase-03-deploy-e-servir-modelos/03-pipeline-treino-deploy-automatico/referencia-productization-lstm
uvicorn sequence_productization_api:app --reload
```

## Arquivos

- `quality_monitor.py`: rolling quality gate para comparar previsão nova e baseline.
- `sequence_productization_api.py`: API FastAPI enxuta inspirada no app de productization da branch de origem.

## Observações didáticas

- o modelo original LSTM foi substituído por um baseline de média móvel para manter o pacote executável sem checkpoints;
- o valor pedagógico aqui está na superfície operacional do serviço: contrato, readiness e quality gate.