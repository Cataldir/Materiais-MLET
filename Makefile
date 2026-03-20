.PHONY: install install-fase01 install-fase02 install-fase03 install-fase04 install-fase05 \
	install-dev lint format test validate-bootstrap notebooks-check clean help

PYTHON ?= python
UV := uv
PIP := pip
DEV_CONSTRAINTS := --constraint constraints/dev.txt
FASE01_CONSTRAINTS := --constraint constraints/fase01.txt --constraint constraints/dev.txt
FASE02_CONSTRAINTS := --constraint constraints/fase02.txt --constraint constraints/dev.txt
FASE03_CONSTRAINTS := --constraint constraints/fase03.txt --constraint constraints/dev.txt
FASE04_CONSTRAINTS := --constraint constraints/fase04.txt --constraint constraints/dev.txt
FASE05_CONSTRAINTS := --constraint constraints/fase05.txt --constraint constraints/dev.txt
ALL_CONSTRAINTS := --constraint constraints/fase01.txt --constraint constraints/fase02.txt --constraint constraints/fase03.txt --constraint constraints/fase04.txt --constraint constraints/fase05.txt --constraint constraints/dev.txt

help:  ## Show this help message
	$(PYTHON) tools/repo_tasks.py make-help

install:  ## Install all dependencies for all phases
	$(UV) pip install $(ALL_CONSTRAINTS) -e ".[fase01,fase02,fase03,fase04,fase05,dev]"

install-dev:  ## Install only dev dependencies
	$(UV) pip install $(DEV_CONSTRAINTS) -e ".[dev]"

install-fase01:  ## Install Fase 01 dependencies
	$(UV) pip install $(FASE01_CONSTRAINTS) -e ".[fase01,dev]"

install-fase02:  ## Install Fase 02 dependencies
	$(UV) pip install $(FASE02_CONSTRAINTS) -e ".[fase02,dev]"

install-fase03:  ## Install Fase 03 dependencies
	$(UV) pip install $(FASE03_CONSTRAINTS) -e ".[fase03,dev]"

install-fase04:  ## Install Fase 04 dependencies
	$(UV) pip install $(FASE04_CONSTRAINTS) -e ".[fase04,dev]"

install-fase05:  ## Install Fase 05 dependencies
	$(UV) pip install $(FASE05_CONSTRAINTS) -e ".[fase05,dev]"

lint:  ## Run ruff linter
	ruff check .
	ruff format --check .

format:  ## Format code with ruff
	ruff format .
	ruff check --fix .

test:  ## Run all tests
	pytest

validate-bootstrap:  ## Run lightweight bootstrap validation for curation work
	$(PYTHON) tools/repo_tasks.py validate

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

notebooks-check:  ## Run lightweight structural validation for tracked notebooks
	$(PYTHON) tools/repo_tasks.py notebooks-check

clean:  ## Remove build artifacts and cache files
	$(PYTHON) tools/repo_tasks.py clean
