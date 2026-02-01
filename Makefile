TAKEHOME_DIR := original_performance_takehome-main-5452f74

.PHONY: help
help:  ## Display this help screen
	@echo -e "\033[1mAvailable commands:\033[0m"
	@grep -E '^[a-z.A-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}' | sort

.PHONY: format
format:  ## Format code
	uv run ruff format . --exclude $(TAKEHOME_DIR)
	uv run ruff check --fix . --exclude $(TAKEHOME_DIR)

.PHONY: lint
lint:  ## Lint code and type check
	uv run ruff check . --exclude $(TAKEHOME_DIR)
	uv run ruff format --check . --exclude $(TAKEHOME_DIR)
	uv run ty check . --exclude $(TAKEHOME_DIR)

.PHONY: dev-lint
dev-lint: format  ## Format code and type check
	uv run ty check . --exclude $(TAKEHOME_DIR)
