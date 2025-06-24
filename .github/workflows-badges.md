# GitHub Actions Status Badges

Add these badges to your README.md:

```markdown
[![CI](https://github.com/rande/python-simple-ioc/actions/workflows/ci.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/ci.yml)
[![Tests](https://github.com/rande/python-simple-ioc/actions/workflows/tests.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/tests.yml)
[![Test Matrix](https://github.com/rande/python-simple-ioc/actions/workflows/test-matrix.yml/badge.svg)](https://github.com/rande/python-simple-ioc/actions/workflows/test-matrix.yml)
```

## Workflow Descriptions

### ci.yml
- Main CI workflow that runs on every push and PR
- Runs flake8 linting and the standard test suite
- Tests against Python 3.9, 3.10, 3.11, 3.12, and 3.13

### tests.yml
- Comprehensive test workflow with separate jobs for:
  - Linting (flake8 and optional mypy)
  - Core tests (without optional dependencies)
  - Tests with individual extras (flask, jinja2, redis)
  - Tests with all extras installed
  - Documentation build
  - Package build and validation


### test-matrix.yml
- Cross-platform testing (Linux, macOS, Windows)
- Full Python version matrix
- Ensures compatibility across different operating systems

### release.yml
- Triggered on version tags
- Builds and publishes to PyPI
- Includes test PyPI publishing for testing

## Required Secrets

To enable package publishing, add these secrets to your GitHub repository:
- `PYPI_API_TOKEN`: Your PyPI API token for publishing releases
- `TEST_PYPI_API_TOKEN`: Your Test PyPI API token for testing releases