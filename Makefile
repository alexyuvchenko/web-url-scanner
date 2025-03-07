.PHONY: build up down logs

# Docker commands
build:
	docker-compose build

up:
	docker-compose up

up-d:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f

# Help command
help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  up        - Start containers in foreground"
	@echo "  up-d      - Start containers in background"
	@echo "  down      - Stop and remove containers"
	@echo "  logs      - View container logs"
	@echo "  help      - Show this help message"
