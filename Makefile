$(MAKECMDGOALS):
	@pipenv run setup.py $@ $(ARGS)

.PHONY: $(MAKECMDGOALS)
