# 02 — Gerenciamento de Dependências em ML

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Poucas coisas corroem tanto a confiabilidade de um projeto de ML quanto ambientes inconsistentes. Esta disciplina trata da base operacional que garante reprodutibilidade: isolamento, pinagem, resolução de conflito e escolha consciente de ferramentas para dependências e build.

## O que você deve aprender

- isolar ambientes de desenvolvimento e execução de forma previsível;
- controlar dependências com `requirements`, `constraints` e ferramentas de empacotamento modernas;
- comparar abordagens com Poetry e uv sem cair em adoção acrítica de ferramenta;
- resolver conflitos e documentar um checklist realista de reprodutibilidade.

## Como usar este material

1. Siga a ordem das aulas, porque a disciplina evolui de fundamentos para casos de conflito.
2. Reproduza os cenários localmente para sentir a diferença entre gestão ad hoc e gestão controlada.
3. Use os exemplos desta trilha como referência quando um projeto do curso exigir ambiente mais formalizado.
4. Trate os checklists como instrumentos de operação, não apenas de estudo.

## Como referenciar esta disciplina no repositório

- O índice da disciplina está em `fase-02-feature-engineering-versionamento/02-gerenciamento-dependencias/`.
- Ao citar uma solução específica, aponte para a aula e para os arquivos de configuração relevantes.
- O README organiza a navegação; os exemplos concretos vivem nas subpastas e nos arquivos de lock/configuração.
- Regras de prontidão e padrão de material continuam centralizadas fora deste clone.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Em operações reais, dependências mal geridas geram incidentes, atrasam deploy e comprometem auditoria. Em termos acadêmicos, a disciplina reforça noções de reprodutibilidade computacional e evidencia que resultados válidos precisam ser reproduzíveis por outros avaliadores e colaboradores.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-isolamento-venv/) | Isolamento com venv/virtualenv | notebook, script |
| [02](aula02-pip-requirements/) | pip avançado, requirements.txt, constraints | `requirements.txt`, `constraints.txt` |
| [03](aula03-poetry-vs-uv/) | Poetry vs uv | dois projetos idênticos |
| [04](aula04-conflitos-reproducibilidade/) | Resolução de conflitos, checklist reprodutibilidade | cenários + soluções |
