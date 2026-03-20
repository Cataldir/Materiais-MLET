# Aula 03 - Otimizacao e quantizacao local

Pacote canonico leve para comparar estrategias de compressao e adaptacao eficiente sem depender de GPU, pesos remotos ou bibliotecas de inferencia pesada.

## Objetivo didatico

- analisar trade-offs entre GPTQ, AWQ e quantizacao dinamica em ambiente local;
- usar perfis heuristicas para estimar memoria, latencia e risco de degradacao;
- comparar quando LoRA ajuda mais do que nova quantizacao.

## O que foi preservado

- vocabulario de otimizacao usado em stacks reais de LLM;
- separacao entre perfil do modelo, hardware e estrategia de compressao;
- comparacao entre adaptacao eficiente e compressao de pesos.

## O que foi simplificado

- download de checkpoints e kernels especializados;
- benchmarks em GPU;
- fine-tuning real com gradientes.

## Execucao

```bash
cd fase-05-llms-e-agentes/01-deploy-modelos-ia-generativa/aula03-otimizacao-quantizacao
python quantization.py
python lora_finetuning.py
```

## Arquivos

- `quantization.py`: aplica Strategy + Template Method sobre perfis locais de modelos.
- `lora_finetuning.py`: compara configuracoes LoRA de forma deterministica.

## Observacoes didaticas

- GPTQ tende a priorizar footprint e agressividade de compressao;
- AWQ favorece equilibrio quando a qualidade precisa se manter mais estavel;
- LoRA faz mais sentido quando a necessidade principal e adaptar comportamento sem reescrever toda a base.