# Aula 04 - Logging, metricas e autenticacao em servicos de inferencia

Pack canonico para tratar preocupacoes transversais de uma API de ML: autenticar, medir e registrar o que acontece sem poluir a regra principal de negocio. O material usa Decorator e Chain of Responsibility para deixar essas responsabilidades visiveis.

## O que foi preservado

- autenticacao por token antes da inferencia;
- contagem de metricas de sucesso e rejeicao;
- logs estruturados em torno do handler principal.

## O que foi simplificado

- sem JWT real, Prometheus ou OpenTelemetry;
- sem servidor HTTP ou middlewares de framework;
- foco em composicao local de responsabilidades transversais.

## Execucao

```bash
cd fase-01-fundamentos-de-ml/04-apis-inferencia-modelos/aula04-logging-metricas-auth
python service_observability_demo.py
```

## Arquivos

- `service_observability_demo.py`: pipeline local com autenticacao, metricas e logs.

## Observacoes didaticas

- observabilidade e seguranca devem envolver o handler, nao contaminar a regra de negocio;
- uma cadeia simples ajuda a visualizar ordem e responsabilidade de cada passo.