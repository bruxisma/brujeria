docs:
	@sphinx-build -M html "docs" "build"

test:
	@python setup.py test

build:
	@python setup.py build

all: build docs test 

.PHONY: help docs test build