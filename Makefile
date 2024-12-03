ifneq (,$(wildcard ./.env))
    include .env
    export
endif

.env:
	cp env.example .env

.PHONY: dev-server
dev-server: .env
	uv run fastapi dev app/main.py

.PHONY: lint
lint:
	uv run ruff check .
	uv run ruff format --check --diff .

.PHONY: fix
fix:
	uv run ruff check . --fix --fix-only --show-fixes
	uv run ruff format .

.PHONY: types
types:
	uv run mypy .

.PHONY: security-checks
security-checks:
	uv run bandit -c pyproject.toml -r .

.PHONY: tests
tests:
	uv run pytest

.PHONY: db-cli
db-cli:
	pgcli "postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${POSTGRES_HOST}:${POSTGRES_PORT}/${POSTGRES_DB}"

.PHONY: gen-migration
gen-migration: message =
gen-migration:
	uv run alembic revision --autogenerate -m "$(message)"

.PHONY: migrate
migrate:
	uv run alembic upgrade head
