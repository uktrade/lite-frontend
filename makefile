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

run_unit_tests_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)

run_unit_tests_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)

run_unit_tests_core:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)

run_ui_tests_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/caseworker $(ARGUMENTS)

run_ui_tests_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/exporter $(ARGUMENTS)

run_ui_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/caseworker
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/exporter

run_all_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/caseworker
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/exporter

secrets:
	cp example.caseworker.env caseworker.env
	cp example.exporter.env exporter.env
