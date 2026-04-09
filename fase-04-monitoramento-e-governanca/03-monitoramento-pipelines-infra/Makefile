.PHONY: up down build train predict logs clean

COMPOSE = docker compose -f infra/docker/docker-compose.yml

## Sobe todo o stack (Prometheus, Grafana, MLflow, Training, Inference)
up: build
	$(COMPOSE) up -d
	@echo ""
	@echo "=== Stack disponivel ==="
	@echo "Grafana:    http://localhost:3000 (admin/admin)"
	@echo "Prometheus: http://localhost:9090"
	@echo "MLflow:     http://localhost:5000"
	@echo "Inference:  http://localhost:8000/docs"
	@echo ""

## Build das imagens Docker
build:
	$(COMPOSE) build

## Derruba todo o stack
down:
	$(COMPOSE) down -v

## Executa o pipeline de treino
train:
	$(COMPOSE) run --rm training

## Envia uma predicao de teste
predict:
	curl -s -X POST http://localhost:8000/predict \
		-H "Content-Type: application/json" \
		-d '{"features": [5.1, 3.5, 1.4, 0.2]}' | python -m json.tool

## Envia um batch de predicoes
predict-batch:
	curl -s -X POST http://localhost:8000/predict/batch \
		-H "Content-Type: application/json" \
		-d '{"instances": [[5.1,3.5,1.4,0.2],[6.2,3.4,5.4,2.3],[5.9,3.0,4.2,1.5]]}' | python -m json.tool

## Mostra logs de todos os servicos
logs:
	$(COMPOSE) logs -f

## Limpa volumes e dados
clean: down
	docker volume prune -f

## Ajuda
help:
	@echo "Comandos disponiveis:"
	@echo "  make up            - Sobe todo o stack"
	@echo "  make down          - Derruba todo o stack"
	@echo "  make build         - Build das imagens Docker"
	@echo "  make train         - Executa pipeline de treino"
	@echo "  make predict       - Envia predicao de teste"
	@echo "  make predict-batch - Envia batch de predicoes"
	@echo "  make logs          - Mostra logs de todos os servicos"
	@echo "  make clean         - Limpa volumes e dados"
