docs:
	@sphinx-build -M html "docs" "build"

test:
	@python setup.py test

build:
	@python setup.py build

clean:
	@python setup.py clean

all: build docs test 

.PHONY: help docs test build