clean: clean-build clean-pyc

clean-build:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

pep8:
	flake8 --exclude=migrations mmc

release: clean
	python setup.py register sdist upload --sign
	python setup.py bdist_wheel upload --sign

sdist: clean
	python setup.py sdist
	ls -l dist

run_server:
	cd demo && python manage.py runserver --traceback

run_shell:
	cd demo && python manage.py shell_plus --print-sql
