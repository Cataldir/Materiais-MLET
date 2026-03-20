# 04 — APIs para Inferência de Modelos

> 4h de vídeo · 4 aulas

## Por que esta disciplina importa

Um modelo só gera valor recorrente quando pode ser consumido por outros sistemas, times e jornadas de negócio. Esta disciplina apresenta a camada de serviço que transforma uma lógica de inferência em produto acessível, testável e monitorável.

## O que você deve aprender

- entender fundamentos de HTTP e REST aplicados a serving de modelos;
- comparar abordagens com Flask e FastAPI para exposição de inferência;
- estruturar schemas, health checks e testes para APIs de ML;
- instrumentar autenticação, logging e métricas básicas de serviço.

## Como usar este material

1. Comece pelos exemplos mínimos para fixar protocolo e estrutura.
2. Em seguida, avance para a API completa com `predict`, testes e middleware.
3. Use a última aula para entender preocupações de operação, não apenas de implementação.
4. Reaproveite estes exemplos nas fases de deploy, CI/CD e monitoramento.

## Como referenciar esta disciplina no repositório

- O caminho canônico é `fase-01-fundamentos-de-ml/04-apis-inferencia-modelos/`.
- Ao citar um padrão específico, referencie a aula correspondente, porque cada uma cobre um bloco técnico distinto.
- Use este README para contextualização e as pastas de aula para demonstrar implementação.
- Critérios de avaliação e precedência documental seguem a governança principal do curso.

## Referenciais teóricos da disciplina

- Consulte o índice local em [referencias/README.md](referencias/README.md) para organizar leituras e documentação de apoio desta disciplina.
- Classifique as fontes nos grupos `Base`, `Complementar`, `Operacional` e `Contextual`, mantendo o padrão canônico do repositório.

## Relevância para a prática executiva e acadêmica

No mercado, a capacidade de expor inferência por API é uma fronteira direta entre protótipo e produto. Em termos acadêmicos, a disciplina mostra como encapsular modelos em interfaces explícitas, uma habilidade central para estudar integração, confiabilidade e medição de sistemas sociotécnicos baseados em ML.

## Aulas

| Aula | Tema | Arquivos |
|------|------|---------|
| [01](aula01-http-rest-flask-fastapi/) | HTTP, REST, Flask vs FastAPI | `hello_flask.py`, `hello_fastapi.py` |
| [02](aula02-microservicos-schemas/) | Microserviços, Pydantic, Health Checks | `schemas.py`, `health_endpoints.py` |
| [03](aula03-api-completa/) | FastAPI completa: model + /predict + testes | `api.py`, `test_api.py` |
| [04](aula04-logging-metricas-auth/) | Logging, Métricas, Auth | `middleware.py`, `auth.py` |
