.PHONY: run
run:
	python manage.py runserver

.PHONY: shell
shell:
	python manage.py shell

.PHONY: test
test: pep8
	python runtests.py	

.PHONY: install
install:
	python setup.py develop

.PHONY: pep8
pep8:
	@flake8 quokka --ignore=F403 --exclude=migrations

.PHONY: sdist
sdist: test
	@python setup.py sdist upload

.PHONY: clean
clean:
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
