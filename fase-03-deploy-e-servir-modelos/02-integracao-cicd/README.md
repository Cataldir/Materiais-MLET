# 02 — Integração com CI/CD

> 5h de vídeo · 5 aulas

## Por que esta disciplina importa

Sem automação, a qualidade de um projeto depende demais de disciplina manual e memória do time. Esta disciplina mostra como CI/CD transforma checks de qualidade, testes, build e deploy em rotina previsível, reduzindo regressão e tornando a entrega de ML mais confiável.

## O que você deve aprender

- estruturar pipelines de integração contínua para projetos de ML;
- usar GitHub Actions e workflows equivalentes para automatizar verificações;
- incorporar testes e gates de qualidade ao ciclo de entrega;
- entender padrões de entrega contínua e deploy controlado, como blue-green.

## Como usar este material

1. Comece pelos fundamentos de CI e pelos exemplos mínimos de workflow.
2. Evolua para qualidade em CI antes de automatizar deploy.
3. Use o pipeline completo como peça integradora da disciplina.
4. Releia esta trilha junto com deploy e monitoramento para conectar entrega e operação.

## Como referenciar esta disciplina no repositório

- O caminho base é `fase-03-deploy-e-servir-modelos/02-integracao-cicd/`.
- Ao citar exemplos concretos, referencie o workflow ou a aula correspondente.
- O README sintetiza propósito e uso; os arquivos YAML e scripts materializam a automação.
- As políticas formais do curso continuam centralizadas na governança canônica.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

Executivamente, CI/CD reduz tempo de feedback e custo de erro tardio. Academicamente, a disciplina permite discutir qualidade de software experimental em termos observáveis, com critérios reproduzíveis de validação, build e release.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-fundamentos-ci/) | Fundamentos CI: lint + test | `README.md`, `.github/workflows/ci.yml`, `ci_fundamentals.py`, notebook |
| [02](aula02-github-actions-ml/) | GitHub Actions para ML | workflows ML |
| [03](aula03-testes-qualidade-ci/) | Testes de qualidade no CI | scripts de teste |
| [04](aula04-cd-deploy/) | CD: deploy automático, blue-green | `cd-deploy.yml` |
| [05](aula05-pipeline-completo/) | Projeto CI/CD completo | `full-ml-pipeline.yml` |
