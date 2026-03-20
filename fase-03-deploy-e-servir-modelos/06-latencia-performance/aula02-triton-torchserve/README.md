# Aula 02 - Triton e TorchServe

Pacote canonico local para comparar dois adapters de serving especializados. A implementacao foca contrato de serving e trade-offs operacionais, sem subir servidores reais.

## Objetivo didatico

- comparar empacotamento e throughput modelado entre Triton e TorchServe;
- usar adapters para manter o mesmo payload de inferencia;
- discutir batching e artefatos de publicacao sem dependencias pesadas.

## O que foi preservado

- comparacao entre dois servidores especializados;
- contrato comum para o mesmo payload de inferencia;
- diferenca entre foco em batching e foco em model archive.

## O que foi simplificado

- sem Triton, TorchServe, Docker ou GPU;
- sem serializacao de modelos reais;
- apenas comparacao local deterministica.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/06-latencia-performance/aula02-triton-torchserve
python serving_adapters.py
```

## Arquivos

- `serving_adapters.py`: compara adapters locais inspirados em Triton e TorchServe.

## Observacoes didaticas

- adapters ajudam a comparar servidores com o mesmo contrato de entrada;
- throughput nao depende so do modelo, mas tambem do runtime e do empacotamento;
- batching dinamico e archive de modelo resolvem problemas diferentes.