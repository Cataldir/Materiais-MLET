# 06 — Latência e Performance — Dados Não Estruturados

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Workloads com imagem, texto e deep learning costumam trazer custos e restrições de latência muito diferentes dos cenários tabulares. Esta disciplina trata de otimização como parte do design do sistema, mostrando que performance é requisito funcional quando o modelo precisa servir com escala e previsibilidade.

## O que você deve aprender

- aplicar técnicas de otimização como quantização, ONNX e pruning;
- comparar servidores especializados para inferência de modelos pesados;
- otimizar pré-processamento de dados não estruturados;
- medir performance de ponta a ponta com benchmarks coerentes.

## Como usar este material

1. Comece pelas técnicas de otimização para entender o impacto no artefato do modelo.
2. Avance para servidores especializados e compare suas propostas.
3. Trate pré-processamento como parte essencial da latência total.
4. Use o benchmark final para consolidar uma visão sistêmica de gargalos.

## Como referenciar esta disciplina no repositório

- O caminho canônico é `fase-03-deploy-e-servir-modelos/06-latencia-performance/`.
- Ao citar uma técnica específica, referencie a aula em que ela é demonstrada e o script principal associado.
- O README organiza o percurso; os benchmarks, handlers e scripts mostram a evidência operacional.
- Regras acadêmicas e de governança seguem fora desta trilha.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Na prática, essa disciplina ajuda a controlar custo computacional e experiência do usuário em produtos de IA mais pesados. Em termos acadêmicos, ela reforça avaliação experimental orientada a desempenho, permitindo discutir throughput, latência e otimização de forma replicável.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-quantizacao-onnx/) | Quantização, ONNX, pruning | `convert_to_onnx.py`, `benchmark.py` |
| [02](aula02-triton-torchserve/) | Triton, TorchServe | configs + handlers |
| [03](aula03-preprocessing-otimizado/) | Pré-processamento imagem/texto | `image_preprocessing.py`, `text_preprocessing.py` |
| [04](aula04-benchmark-completo/) | Benchmark completo | `benchmark_e2e.py` |
