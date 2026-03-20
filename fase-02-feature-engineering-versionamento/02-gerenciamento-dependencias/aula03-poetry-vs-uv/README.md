# Aula 03 - Poetry vs uv

Pack comparativo para discutir escolha de ferramenta sem depender de benchmark ao vivo ou internet. O material usa Strategy para representar duas abordagens de empacotamento sobre o mesmo projeto de exemplo.

## Objetivo didatico

- comparar comandos e contratos de reproducao entre Poetry e uv;
- mostrar que a escolha de ferramenta precisa ser explicada, nao so copiada;
- manter um projeto de exemplo identico para as duas estrategias.

## Execucao

```bash
cd fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/aula03-poetry-vs-uv
python dependency_strategy.py
```

## Arquivos

- `dependency_strategy.py`: compara as duas estrategias usando o mesmo projeto.
- `poetry_project/pyproject.toml`: exemplo para fluxo com Poetry.
- `uv_project/pyproject.toml`: exemplo equivalente para fluxo com uv.

## Observacoes didaticas

- o comparativo enfatiza experiencia operacional e lockfile, nao marketing de ferramenta;
- ambos os projetos usam o mesmo conjunto de dependencias para evitar vies de exemplo;
- o criterio correto e alinhamento com velocidade, governanca e reproducao da equipe.