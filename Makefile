# Configuration
PYTHON = python3
VENV = .venv
VENV_BIN = $(VENV)/bin
PYTHON_VENV = $(VENV_BIN)/python

# OS specific commands
ifeq ($(OS),Windows_NT)
    VENV_BIN = $(VENV)/Scripts
    PYTHON_VENV = $(VENV_BIN)/python.exe
	RM = rmdir /s /q
	ACTIVATE = $(VENV_BIN)/activate.bat
else
	RM = rm -rf
	ACTIVATE = . $(VENV_BIN)/activate
endif

.PHONY: all
all: install

.PHONY: venv
venv:
	@echo "Creating virtual environment..."
	@$(PYTHON) -m venv $(VENV)
	@$(PYTHON_VENV) -m pip install --upgrade pip
	@echo "Virtual environment created at $(VENV)"

.PHONY: install
install: venv
	@echo "Installing package and dependencies..."
	@$(PYTHON_VENV) -m pip install -e ".[dev]"
	@$(PYTHON_VENV) -m pre-commit install
	@echo "Installation complete!"

.PHONY: install-test
install-test: venv
	@echo "Installing package with test dependencies only..."
	@$(PYTHON_VENV) -m pip install -e ".[test]"

.PHONY: format
format:
	@echo "Formatting code..."
	@$(PYTHON_VENV) -m black .
	@$(PYTHON_VENV) -m isort .
	@$(PYTHON_VENV) -m ruff check --fix .
	@echo "Formatting complete!"

.PHONY: lint
lint:
	@echo "Running linters and type checks..."
	@$(PYTHON_VENV) -m black . --check
	@$(PYTHON_VENV) -m isort . --check
	@$(PYTHON_VENV) -m ruff check .
	@$(PYTHON_VENV) -m mypy .
	@echo "Linting complete!"

.PHONY: test
test:
	@echo "Running tests..."
	@$(PYTHON_VENV) -m pytest
	@echo "Tests complete!"

.PHONY: coverage
coverage:
	@echo "Running tests with coverage..."
	@$(PYTHON_VENV) -m pytest --cov=root2csv --cov-report=html
	@echo "Coverage report generated in htmlcov/index.html"

.PHONY: clean
clean:
	@echo "Cleaning up..."
	@$(RM) build dist *.egg-info .eggs .coverage .pytest_cache .ruff_cache .mypy_cache htmlcov 2>/dev/null || true
	@find . -type d -name __pycache__ -exec $(RM) {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@echo "Clean complete!"

.PHONY: clean-venv
clean-venv: clean
	@echo "Removing virtual environment..."
	@$(RM) $(VENV) 2>/dev/null || true
	@echo "Virtual environment removed!"

.PHONY: build
build: clean
	@echo "Building distribution..."
	@$(PYTHON_VENV) -m build
	@echo "Build complete!"

.PHONY: publish-test
publish-test: build
	@echo "Publishing to Test PyPI..."
	@$(PYTHON_VENV) -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

.PHONY: publish
publish: build
	@echo "Publishing to PyPI..."
	@$(PYTHON_VENV) -m twine upload dist/*

.PHONY: generate-test
generate-test:
	@echo "Generating test data..."
	@$(PYTHON_VENV) dev/generate/create_graph.py
	@$(PYTHON_VENV) dev/generate/create_grapherrors.py
	@$(PYTHON_VENV) dev/generate/create_ttree.py
	@echo "Test data generated!"

.PHONY: help
help:
	@echo "Available commands:"
	@echo "  make install         - Create venv and install all dependencies"
	@echo "  make install-test    - Create venv and install test dependencies only"
	@echo "  make format         - Format code using black, isort, and ruff"
	@echo "  make lint           - Run all linters and type checks"
	@echo "  make test           - Run tests"
	@echo "  make coverage       - Run tests with coverage report"
	@echo "  make generate-test  - Generate test data files"
	@echo "  make clean          - Remove all build, test, and coverage files"
	@echo "  make clean-venv     - Remove virtual environment and all build files"
	@echo "  make build          - Build distribution packages"
	@echo "  make publish-test   - Publish to Test PyPI"
	@echo "  make publish        - Publish to PyPI"