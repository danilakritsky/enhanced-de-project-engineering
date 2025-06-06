# Makefile for Enhanced DE Prompt Engineering Project

.PHONY: all install test check db-up db-down

# Default target: install dependencies and run checks/tests
all: install check test

# Install project dependencies using uv
install:
	@echo "Installing dependencies..."
	uv sync

# Run all pre-commit checks (linting, formatting, tests)
check:
	@echo "Running pre-commit checks..."
	uv run pre-commit run --all-files

# Run the pytest test suite
test:
	@echo "Running tests..."
	uv run python -m pytest tests/

# Start the PostgreSQL test database container
db-up:
	@echo "Starting PostgreSQL container..."
	docker compose -f docker/docker-compose.yml --project-directory docker/ up -d postgres

# Stop the PostgreSQL test database container
db-down:
	@echo "Stopping PostgreSQL container..."
	docker compose -f docker/docker-compose.yml --project-directory docker/ down
