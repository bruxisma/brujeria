$(MAKECMDGOALS):
	@python setup.py $@ $(ARGS)

.PHONY: $(MAKECMDGOALS)