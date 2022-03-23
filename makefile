ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

docker-e2e = docker-compose -p lite -f docker-compose.e2e.yml
wait-for-caseworker = dockerize -wait http://localhost:8200/healthcheck -timeout 5m -wait-retry-interval 5s

manage_caseworker:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py $(ARGUMENTS)

manage_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py $(ARGUMENTS)

clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type d -name "__pycache__" -delete

lint:
	-pipenv run bandit -r . --skip=B101 --exclude=/ui_tests,/unit_tests,/tests_common
	-pipenv run prospector exporter
	-pipenv run prospector caseworker
	-pipenv run black .

autoformat:
	-pipenv run black .

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
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS} $(ARGUMENTS)

run_ui_tests_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS} $(ARGUMENTS)

run_ui_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}

run_all_unit_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)

run_all_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)
	PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
	PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -vv ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}

secrets:
	cp example.caseworker.env caseworker.env
	cp example.exporter.env exporter.env

.PHONY: manage_caseworker manage_exporter clean run_caseworker run_exporter run_unit_tests_caseworker run_unit_tests_exporter run_unit_tests_core run_ui_tests_caseworker run_ui_tests_exporter run_ui_tests run_all_tests

start-caseworker:
	$(docker-e2e) up --build -d

stop-caseworker:
	$(docker-e2e) down --remove-orphans

caseworker-e2e-test:
	@echo "*** Requires starting the caseworker stack, which can be started running: 'make start-caseowkrer' ***"
	$(docker-e2e) exec caseworker bash -c '$(wait-for-caseworker) && pytest playwright_tests/specs/test_smoke.py --video=retain-on-failure --output=/app/playwright_videos'
