all: register upload

register:
	python setup.py register 

upload:
	python setup.py sdist upload
