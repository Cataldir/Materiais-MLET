# Aula 05 - Drift multivariado com estrategias locais

Pacote canonico leve para demonstrar drift multivariado sem depender de modelos pesados. O material compara duas estrategias: uma aproximacao por RBF-MMD e outra por erro de reconstrucao via PCA local, preservando a ideia de comparar estrutura conjunta e nao apenas colunas isoladas.

## Objetivo didatico

- mostrar por que drift multivariado pode aparecer mesmo com sinais univariados discretos;
- comparar duas estrategias interpretableis para detectar mudancas na estrutura conjunta;
- manter um fluxo fixo e testavel para explorar thresholds e severidade.

## O que foi preservado

- uso de Strategy para alternar algoritmos de comparacao;
- Template Method para gerar dados, aplicar estrategias e consolidar ranking;
- dataset sintetico reprodutivel com correlacoes controladas.

## O que foi simplificado

- sem autoencoders ou frameworks de deep learning;
- sem dependencia obrigatoria de SciPy ou bibliotecas especializadas;
- foco em metrica resumida e explicacao operacional do alerta.

## Execucao

```bash
cd fase-04-monitoramento-e-governanca/01-data-drift/aula05-drift-multivariado
python multivariate_drift.py
```

## Arquivos

- `multivariate_drift.py`: comparacao entre MMD local e reconstrucao linear.

## Observacoes didaticas

- o objetivo nao e reproduzir uma implementacao industrial completa, e sim tornar o mecanismo visivel;
- a mudanca correlacional ajuda a justificar a necessidade de metricas multivariadas;
- thresholds pequenos ja capturam degradacao relevante em cenarios sinteticos controlados.