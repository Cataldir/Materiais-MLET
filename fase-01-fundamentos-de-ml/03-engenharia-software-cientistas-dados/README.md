# 03 — Engenharia de Software para Cientistas de Dados

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Modelos ruins podem ser descartados rapidamente; código ruim costuma permanecer caro por muito tempo. Esta disciplina mostra como princípios de engenharia de software reduzem fragilidade, custo de manutenção e dependência de conhecimento tácito em projetos de dados e ML.

## O que você deve aprender

- aplicar princípios de modularidade e refatoração a pipelines analíticos;
- usar versionamento e fluxo de colaboração de forma profissional;
- introduzir testes, lint, validação e checks automáticos em projetos de ML;
- organizar ambientes, configurações e pontos de entrada de maneira previsível;
- estruturar CLIs e logs para tornar workflows mais operáveis.

## Como usar este material

1. Compare exemplos `before/` e `after/` para visualizar o ganho estrutural.
2. Use as aulas de Git e testes como base para qualquer projeto do curso.
3. Execute os exemplos de CLI, logging e configuração quando quiser transformar notebooks em ferramentas reutilizáveis.
4. Trate a disciplina como suporte transversal para todas as fases seguintes.

## Como referenciar esta disciplina no repositório

- O caminho de referência desta trilha é `fase-01-fundamentos-de-ml/03-engenharia-software-cientistas-dados/`.
- Cite a aula correspondente quando o foco for um padrão específico, como testes, workflow ou logging.
- Este README resume intenção pedagógica; os artefatos das aulas mostram a implementação concreta.
- Para regras formais de materiais executáveis, consulte a governança canônica em vez de replicar política nesta pasta.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Do ponto de vista executivo, essa disciplina reduz risco operacional, acelera onboarding e melhora previsibilidade de manutenção. No plano acadêmico, ela introduz rigor metodológico na construção de artefatos computacionais, aproximando projetos de ML de padrões mais maduros de engenharia experimental e de software.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-solid-ml/) | SOLID em ML e Refatoração | `before/spaghetti_model.py`, `after/refactored_model.py` |
| [02](aula02-git-workflow/) | Git, Branching, PR Template, DVC Intro | templates + guia |
| [03](aula03-testes-qualidade/) | pytest, pandera, smoke tests, ruff, pre-commit | suite de testes |
| [04](aula04-gerenciamento-deps/) | venv, Poetry, uv, pyproject.toml, .env | pyproject completo |
| [05](aula05-cli-logging/) | CLI, Pydantic Settings, logging JSON, Makefile | entry point CLI |
