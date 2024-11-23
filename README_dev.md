# root2csv

A Python tool to convert ROOT Trees and Graphs to CSV files.

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- make (optional, but recommended)

### Development Setup

1. Clone the repository:
```bash
git clone https://github.com/MohamedElashri/root2csv
cd root2csv
```

2. Set up the development environment:
```bash
make install
```

This will:
- Create a virtual environment
- Install all development dependencies
- Set up pre-commit hooks

### Alternative Setup (without make)

If you don't have `make` available, you can set up manually:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment (Linux/MacOS)
source .venv/bin/activate
# OR on Windows:
# .venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install
```

### Common Development Tasks

Using make:
```bash
# Format code
make format

# Run linters and type checks
make lint

# Run tests
make test

# Generate test data
make generate-test

# Run tests with coverage report
make coverage

# Clean up build files
make clean

# Remove virtual environment and all build files
make clean-venv
```

Manually (without make):
```bash
# Format code
black .
isort .
ruff check --fix .

# Run linters and type checks
black . --check
isort . --check
ruff check .
mypy .

# Run tests
pytest

# Generate test data
python dev/generate/create_graph.py
python dev/generate/create_grapherrors.py
python dev/generate/create_ttree.py
```

### Project Structure

```
root2csv/
├── .venv/                 # Virtual environment (created by make install)
├── root2csv/             # Main package directory
│   ├── __init__.py
│   ├── cli.py
│   ├── converter.py
│   ├── graphs.py
│   ├── trees.py
│   └── utils.py
├── tests/                # Test directory (I welcome new tests)
├── dev/                  # Development scripts (not included)
│   └── generate/        # Test data generation scripts (not included)
├── .pre-commit-config.yaml  # Pre-commit hooks configuration
├── pyproject.toml       # Project configuration
├── LICENSE
├── MANIFEST.in
├── Makefile
└── README.md
```

### Running the Tool

After installation, you can use the tool:

```bash
# List available trees/graphs in a ROOT file
root2csv -f input.root -l

# Convert a specific tree/graph to CSV
root2csv -f input.root -o output.csv -t treename
```

## Development Workflow

1. Create a new branch for your feature/fix:
```bash
git checkout -b feature-name
```

2. Make your changes and ensure everything works:
```bash
# Format code
make format

# Run checks
make lint

# Run tests
make test
```

3. Commit your changes:
```bash
git add .
git commit -m "Description of changes"
```

Pre-commit hooks will automatically run on commit and ensure code quality.

## Publishing

For maintainers only:

```bash
# Build and publish to Test PyPI
make publish-test

# Build and publish to PyPI
make publish
```