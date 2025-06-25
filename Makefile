all: build upload

build:
	pip install build twine
	rm -rf dist/
	python -m build
	twine check dist/*

upload-prod: build
	export TWINE_USERNAME=__token__
	bash -c 'read -s -p "Enter your Production PyPI token: " TWINE_PASSWORD; echo; export TWINE_PASSWORD; python -m twine upload dist/*'

upload-test: build
	export TWINE_USERNAME=__token__
	bash -c 'read -s -p "Enter your Test PyPI token: " TWINE_PASSWORD; echo; export TWINE_PASSWORD; python -m twine upload --repository testpypi dist/*'

clean:
	rm -rf build/ dist/ *.egg-info/ __pycache__/ .pytest_cache/ .mypy_cache/
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete

test:
	flake8 ioc/ tests/
	python -m unittest discover -s tests -p "test_*.py"
	sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html

test-strict:
	flake8 ioc/ tests/
	mypy ioc/
	python -m unittest discover -s tests -p "test_*.py"
	sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html

lint:
	flake8 ioc/ tests/

typecheck:
	mypy ioc/

unittest:
	python -m unittest discover -s tests -p "test_*.py" -v
