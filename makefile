ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

manage_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py $(ARGUMENTS)

manage_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py $(ARGUMENTS)

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

run_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py collectstatic --no-input && PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200

run_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py collectstatic --no-input && PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py runserver localhost:8300

run_unit_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest unit_tests --cov=. --cov-config=.coveragerc --cov-report=html

secrets:
	cp example.caseworker.env caseworker.env
	cp example.exporter.env exporter.env
