# Aula 05 - Pipeline completo de CI/CD

Pacote canonico local que modela um pipeline completo como pipes-and-filters. Cada etapa transforma um artefato simples ate chegar ao pacote pronto para deploy.

## Objetivo didatico

- mostrar um pipeline completo sem depender de GitHub Actions ou runners remotos;
- separar etapas pequenas e compostas, cada uma com uma responsabilidade clara;
- reforcar a ideia de que CI/CD pode ser testado localmente antes da automacao remota.

## O que foi preservado

- etapas de lint, testes, empacotamento e release;
- transformacao sequencial de um artefato compartilhado;
- contrato observavel de sucesso ou falha por etapa.

## O que foi simplificado

- sem build de imagem, registry ou deployment real;
- sem execucao de ferramentas externas;
- apenas metadados locais e verificacoes deterministicas.

## Execucao

```bash
cd fase-03-deploy-e-servir-modelos/02-integracao-cicd/aula05-pipeline-completo
python local_cicd_pipeline.py
```

## Arquivos

- `local_cicd_pipeline.py`: pipeline local no estilo pipes-and-filters para CI/CD.

## Observacoes didaticas

- cada filtro deve alterar o artefato de forma previsivel;
- etapas pequenas facilitam depuracao e reuso;
- a mesma ideia vale para pipelines remotos mais complexos.