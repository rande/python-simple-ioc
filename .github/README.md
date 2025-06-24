# GitHub Actions CI/CD Setup

This directory contains the complete CI/CD setup for the python-simple-ioc project.

## Workflows Overview

### 🚀 Main CI Workflow (`ci.yml`)
- **Purpose**: Primary continuous integration for every push and PR
- **Features**:
  - Tests against Python 3.9, 3.10, 3.11, and 3.12
  - Runs flake8 linting (required to pass)
  - Executes core tests using smart dependency detection
  - Optional mypy type checking (non-blocking)

### 🧪 Comprehensive Testing (`tests.yml`)
- **Purpose**: Detailed testing with multiple configurations and optional dependencies
- **Jobs**:
  - **Lint**: Flake8 and optional mypy across all Python versions
  - **Core Tests**: Tests without optional dependencies
  - **Specific Extras**: Tests individual optional dependencies (flask, jinja2, redis)
  - **All Extras**: Tests with all optional dependencies installed
  - **Documentation**: Builds Sphinx docs and uploads artifacts
  - **Package**: Validates package building

### 🌍 Cross-Platform Testing (`test-matrix.yml`)
- **Purpose**: Ensure compatibility across operating systems
- **Coverage**: Linux, macOS, and Windows
- **Focus**: Core functionality verification


### 📚 Documentation (`docs.yml`)
- **Purpose**: Build and deploy documentation to GitHub Pages
- **Features**:
  - Builds Sphinx documentation with warnings as errors
  - Deploys to GitHub Pages on push to main/master
  - Uses proper GitHub Pages permissions and concurrency

### 🏷️ Release Automation (`release.yml`)
- **Purpose**: Automated package building and PyPI publishing
- **Triggers**: Git tags (version tags)
- **Features**:
  - Runs full test suite before releasing
  - Builds and validates package
  - Publishes to Test PyPI first (if token available)
  - Publishes to PyPI for tagged releases

## Smart Dependency Handling

### Problem Solved
The project has optional dependencies (flask, jinja2, redis) that may not be installed in all environments. Traditional test runs would fail with import errors.

### Solution
- **Workflow-Level Detection**: CI jobs check for dependency availability before running tests
- **Graceful Degradation**: Tests skip gracefully when dependencies are missing
- **Clear Reporting**: Distinguish between real failures and expected missing dependencies
- **Smart Test Scripts**: Embedded test runners in workflows that detect available dependencies

### Usage Examples

```bash
# Run core tests only (no optional dependencies)
python -m unittest discover -s tests -p "test_*.py" | grep -v "extra\."

# Run all tests with make targets
make test

# Run linting only
make lint
```

## Repository Setup Requirements

### Required Secrets (for release automation)
Add these to your GitHub repository settings:
- `PYPI_API_TOKEN`: Your PyPI API token for publishing releases
- `TEST_PYPI_API_TOKEN`: Your Test PyPI API token for testing

### GitHub Pages Setup
1. Go to repository Settings → Pages
2. Select "GitHub Actions" as the source
3. The `docs.yml` workflow will automatically deploy documentation

### Branch Protection
Consider setting up branch protection rules for `main`/`master`:
- Require status checks: CI workflow must pass
- Require up-to-date branches before merging
- Include administrators in restrictions

## Status Badges

Add these to your README.md:

```markdown
[![CI](https://github.com/rande/python-simple-ioc/actions/workflows/ci.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/ci.yml)
[![Tests](https://github.com/rande/python-simple-ioc/actions/workflows/tests.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/tests.yml)
[![Docs](https://github.com/rande/python-simple-ioc/actions/workflows/docs.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/docs.yml)
[![Test Matrix](https://github.com/rande/python-simple-ioc/actions/workflows/test-matrix.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/test-matrix.yml)
```

## Maintenance

### Dependabot
Automated dependency updates are configured in `dependabot.yml`:
- Weekly Python package updates
- Weekly GitHub Actions updates
- Automatic PR creation with proper labels

### Local Development
For local development and testing:
```bash
# Install with dev dependencies
pip install -e ".[dev]"

# Run linting
make lint

# Run tests (basic)
make test

# Run tests with type checking
make test-strict

# Run core tests only
python -m unittest discover -s tests -p "test_*.py" | grep -v "extra\."
```