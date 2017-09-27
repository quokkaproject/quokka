.PHONY: docs test pep8 clean install build publish tree create_env devserver

test: pep8
	QUOKKA_MODE=test py.test --cov=quokka -l --tb=short --maxfail=1 tests/

pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

docs:
	@./mdbook build docs/

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf dist/
	@rm -rf *.egg
	@rm -rf *.egg-info

install:
	@pip install flit pypandoc pygments
	@flit install -s

build:
	@flit build

publish:
	@flit publish

tree:
	@tree  -L 1 -a -I __pycache__ --dirsfirst --noreport

create_env:
	@rm -rf venv
	@python3.6 -m venv venv

devserver:
	$(info "Running quokka project template...")
	@cd quokka/project_template; quokka runserver
