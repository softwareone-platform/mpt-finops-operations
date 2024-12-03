.env:
	cp env.example .env

.PHONY: dev-server
dev-server:
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
