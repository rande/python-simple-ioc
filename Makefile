all: register upload

register:
	python setup.py register 

upload:
	python setup.py sdist upload

test:
	nosetests
	sphinx-build -nW -b html -d docs/_build/doctrees docs docs/_build/html