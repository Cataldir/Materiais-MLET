# Aula 01 - Quantizacao e ONNX

Pacote canonico local para demonstrar conversao de modelos sklearn e PyTorch para ONNX e aplicacao de quantizacao para reducao de latencia de inferencia.

## Objetivo didatico

- converter modelos treinados para formato ONNX;
- aplicar quantizacao pos-treino (INT8) para reducao de latencia;
- comparar tempos de inferencia entre modelo original e otimizado.

## O que foi preservado

- pipeline de conversao sklearn para ONNX via skl2onnx;
- benchmark comparativo entre modelo original e ONNX;
- estrutura de CLI para uso em pipelines automatizados.

## O que foi simplificado

- sem modelos PyTorch reais (foco em sklearn);
- sem GPU ou hardware especializado;
- benchmark local deterministico.

## Execucao

```bash
cd fase-03-cloud-e-mlops/06-latencia-performance/aula01-quantizacao-onnx
pip install onnx onnxruntime skl2onnx
python convert_to_onnx.py --model models/model.pkl --output models/model.onnx
```

## Arquivos

- `convert_to_onnx.py`: conversao de modelos para ONNX e benchmark de latencia.

## Observacoes didaticas

- ONNX e um formato intermediario que permite otimizacoes independentes do framework;
- quantizacao reduz precisao numerica em troca de velocidade, com impacto mensuravel na acuracia;
- a comparacao antes/depois e essencial para justificar a troca em producao.
