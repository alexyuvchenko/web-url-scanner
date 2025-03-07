.PHONY: build up down logs setup-local run-local clean-local help

# Default target
.DEFAULT_GOAL := help

# Docker development commands
build:
	docker-compose build

up:
	docker-compose up

down:
	docker-compose down

logs:
	docker-compose logs -f

# Local development commands
setup-local:
	chmod +x scripts/setup_local.sh
	./scripts/setup_local.sh

run-local:
	@if [ -d ".venv" ]; then \
		source .venv/bin/activate && python -m web_url_scanner.scanner; \
	else \
		echo "Virtual environment not found. Run 'make setup-local' first."; \
		exit 1; \
	fi

clean-local:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Help command
help:
	@echo "Available commands:"
	@echo "Docker commands:"
	@echo "  build        - Build Docker images"
	@echo "  up           - Start containers"
	@echo "  down         - Stop containers"
	@echo "  logs         - View container logs"
	@echo ""
	@echo "Local development commands:"
	@echo "  setup-local  - Set up local development environment with .venv"
	@echo "  run-local    - Run scanner in local environment"
	@echo "  clean-local  - Remove virtual environment and cache files"
	@echo ""
	@echo "  help         - Show this help message"
