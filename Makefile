docs:
	@sphinx-build -M html "docs" "build"

test:
	@python setup.py test

build:
	@python setup.py build

sdist:
	@python setup.py clean_egg_info sdist

list-dist:
	@python -m tarfile -l dist/brujeria-0.1.tar.gz

clean:
	@python setup.py clean --all

all: build docs test 

.PHONY: help docs test build