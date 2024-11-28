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
