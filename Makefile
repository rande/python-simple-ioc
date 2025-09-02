all: build

build-install:
	uv pip install build twine flake8 sphinx

build: build-install clean
	rm -rf dist/
	uv run python -m build
	uv run twine check dist/*

upload-prod: build-install build
	export TWINE_USERNAME=__token__
	bash -c 'read -s -p "Enter your Production PyPI token: " TWINE_PASSWORD; echo; export TWINE_PASSWORD; uv run twine upload dist/*'

upload-test: build-install build
	export TWINE_USERNAME=__token__
	bash -c 'read -s -p "Enter your Test PyPI token: " TWINE_PASSWORD; echo; export TWINE_PASSWORD; uv run twine upload --repository testpypi dist/*'

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .mypy_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

test: build-install
	uv run flake8 ioc/ tests/
	uv run python -m unittest discover -s tests -p "test_*.py"
	LC_ALL=C.UTF-8 LANG=C.UTF-8 uv run sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html

test-strict: build-install
	uv run flake8 ioc/ tests/
	uv run mypy ioc/
	uv run python -m unittest discover -s tests -p "test_*.py"
	LC_ALL=C.UTF-8 LANG=C.UTF-8 uv run sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html

lint: build-install
	uv run flake8 ioc/ tests/

typecheck: build-install
	uv run mypy ioc/

unittest: build-install
	uv run python -m unittest discover -s tests -p "test_*.py" -v
