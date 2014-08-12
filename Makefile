all: register upload

register:
	python setup.py register 

upload:
	python setup.py sdist upload

test:
	for f in $(find . -name '*.py'); do pyflakes $f; done
	nosetests
	sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html
