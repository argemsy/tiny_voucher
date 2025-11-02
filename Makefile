.PHONY: help init up down build ps logs test lint fmt migrate makemigrations clean prune
.ONESHELL:
SHELL := /bin/bash
.DEFAULT_GOAL := help

PROJECT_NAME := tiny-voucher-backend
SERVICE := api

# Colors
BLUE := \033[36m
RESET := \033[0m

help: ## Show available commands
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_.-]+:.*?## / {printf "$(BLUE)%-25s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

# ------------------------------------------------------------------------------

init: down volume up ## Rebuild and start project cleanly

up: pull build ## Run all services
	docker compose up -d
	make ps

down: ## Stop and remove all Docker services
	docker compose down --remove-orphans

volume: ## Remove all containers volumes
	docker volume prune -f

build: ## Build or rebuild services
	docker compose build

ps: ## Show running containers
	docker compose ps

logs: ## Show service logs (use LOGS=srv-name for specific service)
	docker compose logs -f $(LOGS)

prune: ## Remove all volumes, containers and services
	make down
	make volume
	docker system prune -f
# ------------------------------------------------------------------------------

migrate: ## Run Django migrations
	docker compose exec $(SERVICE) python manage.py migrate

makemigrations: ## Create new migrations
	docker compose exec $(SERVICE) python manage.py makemigrations

shell: ## Open Django shell inside container
	docker compose exec $(SERVICE) python manage.py shell_plus || python manage.py shell

# ------------------------------------------------------------------------------

test: ## Run test suite with coverage
	docker compose run --rm $(SERVICE) pytest --cov=src --disable-warnings --cache-clear -v

lint: ## Run all linters (Ruff + Black + Isort + MyPy)
	docker compose run --rm $(SERVICE) sh -c \
		"ruff check src && black --check src && isort --check-only src && mypy src"

fmt: ## Auto-format code (Black + Isort + Ruff fix)
	docker compose run --rm $(SERVICE) sh -c \
		"ruff check --fix src && isort src && black src"

clean: ## Remove caches, pyc files and temporary data
	find . -name '__pycache__' -type d -exec rm -rf {} + || true
	find . -name '*.py[co]' -delete
	find . -name '*~' -delete
	rm -rf .pytest_cache .mypy_cache htmlcov

# ------------------------------------------------------------------------------

deps: ## Install Python dependencies via Poetry
	poetry install --no-root

update-deps: ## Update all Poetry dependencies
	poetry update

# ------------------------------------------------------------------------------

docker-rebuild: ## Force rebuild Docker images without cache
	docker compose build --no-cache
	docker compose up -d

coverage: ## Generate HTML coverage report
	docker compose run --rm $(SERVICE) pytest --cov=src --cov-report=html
	open htmlcov/index.html || true

# ------------------------------------------------------------------------------

ssh-mount: ## Initialize SSH agent for private dependencies
	eval `ssh-agent -s` && ssh-add && ssh-add -L

# ------------------------------------------------------------------------------

lint-dev: ## Run all linters locally (Ruff + Black + Isort + MyPy)
	poetry run ruff check src
	poetry run black --check src
	poetry run isort --check-only src
	poetry run mypy src

fmt-dev: ## Auto-format code locally (Ruff fix + Black + Isort)
	poetry run ruff check --fix src
	poetry run isort src
	poetry run black src

fmt-test: ## Auto-format code locally (Ruff fix + Black + Isort)
	poetry run ruff check --fix tests
	poetry run isort tests
	poetry run black tests
