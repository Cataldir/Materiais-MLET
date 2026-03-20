# 05 — Bibliotecas Internas e SDKs

> 6h de vídeo · 6 aulas

## Por que esta disciplina importa

Projetos maduros de ML não sobrevivem à base de copiar e colar código entre notebooks. Esta disciplina mostra como transformar soluções recorrentes em bibliotecas internas, utilitários e SDKs capazes de padronizar comportamentos, reduzir retrabalho e acelerar a evolução de múltiplos produtos analíticos.

## O que você deve aprender

- identificar duplicação estrutural e oportunidades de abstração útil;
- empacotar utilitários e transformadores em componentes reaproveitáveis;
- documentar código técnico para consumo de outros times e professores;
- versionar, distribuir e evoluir bibliotecas com critérios claros;
- integrar SDKs internos a pipelines de ML e ferramentas de tracking.

## Como usar este material

1. Comece entendendo o problema da duplicação antes de abstrair qualquer coisa.
2. Explore o pacote `ml_utils` como exemplo de reaproveitamento com propósito didático.
3. Use as aulas de documentação e versionamento para aprender a transformar código em ativo organizacional.
4. Feche com a integração entre SDKs e pipelines para enxergar valor sistêmico da disciplina.

## Como referenciar esta disciplina no repositório

- O índice oficial está em `fase-01-fundamentos-de-ml/05-bibliotecas-internas-sdks/`.
- Ao mencionar um padrão específico, cite a aula correspondente ou o diretório principal do pacote envolvido.
- Este README explica o papel da trilha; as subpastas mostram a implementação concreta do empacotamento.
- Questões de governança e política de material permanecem fora desta pasta e devem ser consultadas no repositório principal.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, bibliotecas internas reduzem variabilidade, aumentam velocidade de entrega e ajudam a consolidar práticas comuns entre times. Academicamente, a disciplina introduz noções de modularização, documentação e evolução controlada de artefatos, fundamentais para estudar manutenção e reuso em software intensivo em dados.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-problema-duplicacao/) | Problema do código duplicado | notebook |
| [02](aula02-pacote-ml-utils/) | Pacote `ml_utils` com transformadores custom | `ml_utils/` |
| [03](aula03-documentacao/) | Docstrings, type hints, MkDocs | `mkdocs.yml`, `docs/` |
| [04](aula04-semver-pypi/) | SemVer, CHANGELOG, build, PyPI interno | `pyproject.toml`, `CHANGELOG.md` |
| [05](aula05-formatacao/) | PEP 8, naming, ruff/black | `before/`, `after/` |
| [06](aula06-integracao-sklearn-mlflow/) | Integração sklearn + MLflow + SDKs | `pipeline_with_sdk.py` |
