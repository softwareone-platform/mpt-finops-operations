.env:
	cp env.example .env

.PHONY: dev-server
dev-server:
	uv run fastapi dev app/main.py

.PHONY: lint
lint:
	uv run ruff check .

.PHONY: format
format:
	uv run ruff check . --fix --fix-only --show-fixes
	uv run ruff format .

.PHONY: types
types:
	uv run mypy .

.PHONY: security-checks
security-checks:
	uv run bandit -c pyproject.toml -r .

# TODO: Move to CI once it's set  and store it as artefact
openapi.json:
	uv run python -m scripts.generate_openapi_json openapi.json
