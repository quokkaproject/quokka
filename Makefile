.PHONY: run shell test install pep8 clean

run:
	python manage.py runserver --reloader --debug

shell:
	python manage.py shell

test: pep8
	QUOKKA_MODE=test py.test --cov=quokka -l --tb=short --maxfail=1 quokka/

install:
	python setup.py develop

pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
