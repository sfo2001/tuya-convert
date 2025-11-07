# Makefile for tuya-convert development
#
# Common tasks:
#   make install-dev  - Install development dependencies
#   make test         - Run all tests
#   make format       - Format code with black and isort
#   make lint         - Run all linters
#   make check        - Run tests and linters
#   make clean        - Remove generated files

.PHONY: help install install-dev test test-verbose test-coverage format lint lint-flake8 lint-mypy lint-pylint lint-bandit check clean

# Default target
help:
	@echo "tuya-convert development commands:"
	@echo ""
	@echo "  make install-dev    Install development dependencies"
	@echo "  make test           Run all tests"
	@echo "  make test-verbose   Run tests with verbose output"
	@echo "  make test-coverage  Run tests with coverage report"
	@echo "  make format         Format code with black and isort"
	@echo "  make lint           Run all linters"
	@echo "  make check          Run tests and linters (CI pipeline)"
	@echo "  make clean          Remove generated files"
	@echo ""
	@echo "Individual linters:"
	@echo "  make lint-flake8    Run flake8"
	@echo "  make lint-mypy      Run mypy"
	@echo "  make lint-pylint    Run pylint"
	@echo "  make lint-bandit    Run bandit (security)"

# Installation
install:
	pip install -r requirements.txt

install-dev:
	pip install -r requirements-dev.txt

# Testing
test:
	pytest

test-verbose:
	pytest -vv

test-coverage:
	pytest --cov=scripts --cov-report=html --cov-report=term
	@echo ""
	@echo "Coverage report generated in htmlcov/index.html"

# Formatting
format:
	@echo "Running isort..."
	isort scripts/ tests/
	@echo "Running black..."
	black scripts/ tests/
	@echo "Formatting complete!"

# Linting
lint-flake8:
	@echo "Running flake8..."
	flake8 scripts/ tests/

lint-mypy:
	@echo "Running mypy..."
	mypy scripts/

lint-pylint:
	@echo "Running pylint..."
	pylint scripts/ || true  # Don't fail on warnings

lint-bandit:
	@echo "Running bandit (security)..."
	bandit -r scripts/

lint: lint-flake8 lint-mypy lint-bandit
	@echo "All linters passed!"

# Combined check (for CI)
check: test lint
	@echo "All checks passed!"

# Cleanup
clean:
	@echo "Cleaning up generated files..."
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .coverage
	rm -rf htmlcov
	rm -rf dist
	rm -rf build
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	@echo "Cleanup complete!"
