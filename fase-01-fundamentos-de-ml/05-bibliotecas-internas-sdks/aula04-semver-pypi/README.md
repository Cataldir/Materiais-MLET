# Aula 04 - SemVer, changelog e release interno

Pack canonico para ensinar como uma biblioteca interna evolui com previsibilidade. A aula liga tipo de mudanca, bump de versao, changelog e publicacao simulada em um fluxo unico de release.

## O que foi preservado

- raciocinio de SemVer para patch, minor e major;
- geracao de changelog e artefatos de release;
- uso de Template Method com estado explicito do ciclo de release.

## O que foi simplificado

- sem build wheel real nem push para registry;
- sem credenciais ou infraestrutura de PyPI interno;
- foco em decisao de versao e disciplina de release.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/aula04-semver-pypi
python release_workflow.py
```

## Arquivos

- `release_workflow.py`: calcula a proxima versao e simula o pipeline de publicacao.

## Observacoes didaticas

- release bom comunica mudanca, risco e compatibilidade de forma objetiva;
- SemVer nao elimina julgamento tecnico, mas ajuda a torná-lo explicito e auditavel.