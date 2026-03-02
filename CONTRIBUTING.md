# Contributing to Master Folder Manager

Thank you for your interest in contributing. This guide will help you get started.

## Getting Started

### Prerequisites

- Python 3.9 or higher
- Git
- A GitHub account

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/Master-Folder-Manager.git
cd Master-Folder-Manager

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install with development dependencies
pip install -e ".[dev]"

# Install pre-commit hooks
pre-commit install

# Verify setup
python -m pytest
```

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

### 2. Make Changes

- Write code following the project style (see Code Style below)
- Add or update tests for your changes
- Ensure all tests pass locally

### 3. Test Your Changes

```bash
# Run all tests with coverage
python -m pytest --cov=src --cov-report=term-missing

# Run linting
ruff check src/ tests/
ruff format --check src/ tests/

# Run type checking
mypy src/

# Or run everything via pre-commit
pre-commit run --all-files
```

### 4. Commit and Push

```bash
git add <files>
git commit -m "Brief description of changes"
git push origin feature/your-feature-name
```

### 5. Open a Pull Request

- Fill out the PR template completely
- Link any related issues
- Ensure CI checks pass

## Code Style

### Python

- Follow PEP 8 conventions
- Use type hints for all function signatures
- Write docstrings for public functions and classes (Google style)
- Keep functions focused and under 50 lines where practical
- Use `pathlib.Path` instead of `os.path` for path operations

### Testing

- Use pytest with the fixtures in `tests/conftest.py`
- Follow the Arrange-Act-Assert pattern
- Test both success and failure paths
- Use `tmp_path` for filesystem tests
- Use `monkeypatch` for mocking
- Aim for 95%+ coverage on new code

### Pydantic Models

- Use Pydantic v2 syntax (`field_validator`, `model_validator`, `ConfigDict`)
- Add field descriptions and examples
- Implement proper validation with clear error messages
- Use `model_dump()` (not deprecated `dict()`)

### Commits

- Use clear, descriptive commit messages
- Start with a verb in imperative mood ("Add", "Fix", "Update")
- Reference issue numbers where applicable (`Fixes #123`)

## Pull Request Guidelines

### Requirements

- All CI checks must pass (tests, lint, type check, markdown lint)
- Coverage must not decrease below the threshold (95%)
- At least one approval from a maintainer
- PR description must explain what and why

### Review Process

1. Automated CI checks run on every PR
2. A maintainer will review your code
3. Address any review feedback
4. Once approved, the PR will be merged

### What Makes a Good PR

- Focused on a single concern
- Includes tests for new functionality
- Updates documentation if needed
- Has a clear description

## Reporting Bugs

Use the [bug report template](.github/ISSUE_TEMPLATE/bug_report.md) and include:

- Python version and OS
- Steps to reproduce
- Expected vs actual behavior
- Error messages or logs

## Requesting Features

Use the [feature request template](.github/ISSUE_TEMPLATE/feature_request.md) and include:

- Problem description
- Proposed solution
- Alternatives considered

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
