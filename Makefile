.PHONY: docs test pep8 clean install build publish tree create_env devserver pandoc adduser

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
	@rm -rf build/
	@rm -rf README.rst
	@rm -rf .eggs/
	@rm -rf *.egg
	@rm -rf *.egg-info


reqs:
	@pip install pbr pypandoc pygments

pandoc: reqs
	@pandoc --from=markdown --to=rst --output=README.rst README.md

install: clean pandoc
	@python setup.py develop

build: clean pandoc
	@python setup.py sdist bdist_wheel --universal

publish: build
	@twine upload dist/*

tree:
	@tree  -L 1 -a -I __pycache__ --dirsfirst --noreport

create_env:
	@rm -rf venv
	@python3.6 -m venv venv

devserver:
	$(info "Running quokka project template...")
	@cd quokka/project_template; quokka runserver

shell:
	$(info "Running quokka shell...")
	@cd quokka/project_template; quokka shell


adduser:
	$(info "Running quokka adduser...")
	@cd quokka/project_template; quokka adduser
