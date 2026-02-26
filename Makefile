.PHONY: help install dev-install test lint format docker-build docker-up docker-down clean

help:
	@echo "OpenDocGen - Open Source Document Generation Agent"
	@echo ""
	@echo "Available commands:"
	@echo "  install      Install production dependencies"
	@echo "  dev-install  Install development dependencies"
	@echo "  test         Run test suite"
	@echo "  lint         Run linters"
	@echo "  format       Format code with black and isort"
	@echo "  docker-build Build Docker images"
	@echo "  docker-up    Start all services with Docker Compose"
	@echo "  docker-down  Stop all services"
	@echo "  clean        Clean up temporary files"

install:
	pip install -e .

dev-install:
	pip install -e ".[dev]"
	pre-commit install

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

lint:
	flake8 src tests
	mypy src
	black --check src tests
	isort --check-only src tests

format:
	black src tests
	isort src tests

docker-build:
	docker-compose -f docker/docker-compose.yml build

docker-up:
	docker-compose -f docker/docker-compose.yml up -d
	@echo "Waiting for services to start..."
	@sleep 10
	@if [ "$(OS)" = "Windows_NT" ]; then \
		./scripts/health_check.bat; \
	else \
		./scripts/health_check.sh; \
	fi

docker-down:
	docker-compose -f docker/docker-compose.yml down

docker-logs:
	docker-compose -f docker/docker-compose.yml logs -f

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.egg-info" -delete
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov
	rm -rf build dist *.egg-info

setup:
	@if [ "$(OS)" = "Windows_NT" ]; then \
		./scripts/setup.bat; \
	else \
		./scripts/setup.sh; \
	fi

dev:
	@if [ "$(OS)" = "Windows_NT" ]; then \
		./scripts/dev-start.bat; \
	else \
		./scripts/dev-start.sh; \
	fi

models:
	@if [ "$(OS)" = "Windows_NT" ]; then \
		./scripts/download_models.bat; \
	else \
		./scripts/download_models.sh; \
	fi
