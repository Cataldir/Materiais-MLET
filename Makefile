.PHONY: install install-fase01 install-fase02 install-fase03 install-fase04 install-fase05 \
        install-dev lint format test notebooks-check clean help

PYTHON := python3
UV := uv
PIP := pip

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install all dependencies for all phases
	$(UV) pip install -e ".[fase01,fase02,fase03,fase04,fase05,dev]"

install-dev:  ## Install only dev dependencies
	$(UV) pip install -e ".[dev]"

install-fase01:  ## Install Fase 01 dependencies
	$(UV) pip install -e ".[fase01,dev]"

install-fase02:  ## Install Fase 02 dependencies
	$(UV) pip install -e ".[fase02,dev]"

install-fase03:  ## Install Fase 03 dependencies
	$(UV) pip install -e ".[fase03,dev]"

install-fase04:  ## Install Fase 04 dependencies
	$(UV) pip install -e ".[fase04,dev]"

install-fase05:  ## Install Fase 05 dependencies
	$(UV) pip install -e ".[fase05,dev]"

lint:  ## Run ruff linter
	ruff check .
	ruff format --check .

format:  ## Format code with ruff
	ruff format .
	ruff check --fix .

test:  ## Run all tests
	pytest

test-fase01:  ## Run Fase 01 tests
	pytest fase-01-fundamentos-de-ml/ -v

test-fase02:  ## Run Fase 02 tests
	pytest fase-02-feature-engineering-versionamento/ -v

test-fase03:  ## Run Fase 03 tests
	pytest fase-03-deploy-e-servir-modelos/ -v

test-fase04:  ## Run Fase 04 tests
	pytest fase-04-monitoramento-e-governanca/ -v

test-fase05:  ## Run Fase 05 tests
	pytest fase-05-llms-e-agentes/ -v

notebooks-check:  ## Check that all notebooks can be executed (requires nbconvert)
	find . -name "*.ipynb" -not -path "*/.ipynb_checkpoints/*" \
		-exec jupyter nbconvert --to notebook --execute {} \; 2>&1 | grep -E "(ERROR|OK)"

clean:  ## Remove build artifacts and cache files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name ".pytest_cache" -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build/ dist/ .coverage htmlcov/
