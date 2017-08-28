.PHONY: test pep8 clean prepare build publish

test: pep8
	QUOKKA_MODE=test py.test --cov=quokka -l --tb=short --maxfail=1 tests/

pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf dist/
	@rm -rf *.egg
	@rm -rf *.egg-info

prepare:
	@pip install flit pypandoc
	@flit install -s

build:
	@flit build

publish:
	@flit publish
