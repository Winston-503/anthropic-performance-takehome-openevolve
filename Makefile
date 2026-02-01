.PHONY: format
format:  ## Format code
	uv run ruff format . --exclude original_performance_takehome-main-5452f74
	uv run ruff check --fix . --exclude original_performance_takehome-main-5452f74

.PHONY: lint
lint:  ## Lint code and type check
	uv run ruff check . --exclude original_performance_takehome-main-5452f74
	uv run ruff format --check . --exclude original_performance_takehome-main-5452f74
	uv run ty check . --exclude original_performance_takehome-main-5452f74

.PHONY: dev-lint
dev-lint: format  ## Format code and type check
	uv run ty check . --exclude original_performance_takehome-main-5452f74
