.PHONY: docs test pep8 clean install build publish tree createvenv devserver pandoc adduser develop

test: pep8
	QUOKKA_MODE=test pytest --cov=quokka -l --tb=short --maxfail=1 tests/

pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

docs:
	@./mdbook build docs/

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf dist/
	@rm -rf build/
	@rm -rf README.rst
	@rm -rf .eggs/
	@rm -rf *.egg
	@rm -rf *.egg-info


develop:
	@. .venv/bin/activate
	@pip install --upgrade pip
	@pip install -r requirements.txt
	@pip install -r requirements-dev.txt
	@pip freeze

reqs:
	@pip install pbr pypandoc pygments

pandoc: reqs
	@pandoc --from=markdown --to=rst --output=README.rst README.md

install:
	@python3.6 setup.py develop

build:
	@python3.6 setup.py sdist bdist_wheel --universal

publish: build
	@twine upload dist/*

tree:
	@tree  -L 1 -a -I __pycache__ --dirsfirst --noreport

createvenv:
	@rm -rf .venv
	@python3.6 -m venv .venv
	@. .venv/bin/activate
	@ls -lparth

devserver:
	$(info "Running quokka project template...")
	@cd quokka/project_template; quokka runserver

shell:
	$(info "Running quokka shell...")
	@cd quokka/project_template; quokka shell


adduser:
	$(info "Running quokka adduser...")
	@cd quokka/project_template; quokka adduser
