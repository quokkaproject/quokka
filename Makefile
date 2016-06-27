.PHONY: run shell test pep8 clean

run:
	manage runserver --reloader --debug

shell:
	manage shell

test: pep8
	QUOKKA_MODE=test py.test --cov=quokka -l --tb=short --maxfail=1 quokka/

pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
