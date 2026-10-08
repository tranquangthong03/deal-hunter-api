cat > Makefile << 'EOF'
.PHONY: help install dev up down logs test lint format migrate seed clean

help:
	@echo "Available commands:"
	@echo "  make install    - Install dependencies"
	@echo "  make dev        - Run API in dev mode"
	@echo "  make up         - Start all services with Docker"
	@echo "  make down       - Stop all services"
	@echo "  make logs       - View logs"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make migrate    - Run DB migrations"
	@echo "  make seed       - Seed mock data"
	@echo "  make clean      - Clean cache files"

install:
	pip install -r requirements.txt
	pre-commit install

dev:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

test:
	pytest

lint:
	ruff check app tests
	mypy app

format:
	ruff format app tests
	ruff check --fix app tests

migrate:
	alembic upgrade head

seed:
	python -m scripts.seed_mock_data

clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov .mypy_cache .ruff_cache
EOF