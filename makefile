ARGUMENTS = $(filter-out $@,$(MAKECMDGOALS)) $(filter-out --,$(MAKEFLAGS))

ifdef CI
	docker-e2e-caseworker = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.yml -f docker-compose.caseworker.yml
	docker-e2e-exporter = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.yml -f docker-compose.exporter.yml
	docker-e2e-caseworker-dbt-plafform = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.dbt.platform.yml -f docker-compose.caseworker.yml -f docker-compose.dbt-platform.yml
	docker-e2e-exporter-dbt-plafform = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.dbt.platform.yml -f docker-compose.exporter.yml -f docker-compose.dbt-platform.yml
else
	docker-e2e-caseworker = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.yml -f docker-compose.caseworker.yml
	docker-e2e-exporter = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.yml -f docker-compose.exporter.yml
	docker-e2e-caseworker-dbt-plafform = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.dbt.platform.yml -f docker-compose.caseworker.yml -f docker-compose.dbt-platform.yml
	docker-e2e-exporter-dbt-plafform = docker-compose -p lite -f docker-compose.base.yml -f docker-compose.api.dbt.platform.yml -f docker-compose.exporter.yml -f docker-compose.dbt-platform.yml
endif

wait-for-caseworker = dockerize -wait http://caseworker:8200/healthcheck -timeout 10m -wait-retry-interval 5s
wait-for-exporter = dockerize -wait http://exporter:8300/healthcheck -timeout 10m -wait-retry-interval 5s

ifdef CI
	start-command = up --build --force-recreate -d
else
	start-command = up --build --force-recreate
endif

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
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS} $(ARGUMENTS)

run_ui_tests_exporter:
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS} $(ARGUMENTS)

run_ui_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}

run_js_tests:
	npm run test

run_docker_ui_tests:
	docker-compose exec caseworker bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}"
	docker-compose exec exporter bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}"

run_all_unit_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)

run_all_tests:
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ./unit_tests/caseworker --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/exporter --cov=. --cov-config=.coveragerc --cov-report=html
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest ./unit_tests/core --cov=. --cov-config=.coveragerc --cov-report=html -vv $(ARGUMENTS)
	PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest -vv ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
	PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest -vv ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}

secrets:
	cp example.caseworker.env caseworker.env
	cp example.exporter.env exporter.env

.PHONY: manage_caseworker manage_exporter clean run_caseworker run_exporter run_unit_tests_caseworker run_unit_tests_exporter run_unit_tests_core run_ui_tests_caseworker run_ui_tests_exporter run_ui_tests run_all_tests

start-caseworker:
	$(docker-e2e-caseworker) $(start-command)

start-caseworker-dbt-platform:
	$(docker-e2e-caseworker-dbt-plafform) $(start-command)

stop-caseworker:
	$(docker-e2e-caseworker) down --remove-orphans

start-exporter:
	$(docker-e2e-exporter) $(start-command)

start-exporter-dbt-platform:
	$(docker-e2e-exporter-dbt-plafform) $(start-command)

stop-exporter:
	$(docker-e2e-exporter) down --remove-orphans

caseworker-e2e-selenium-test:
	@echo "*** Requires starting the caseworker stack, which can be started running: 'make start-caseworker' ***"
	$(docker-e2e-caseworker) exec caseworker bash -c '$(wait-for-caseworker)' && PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest --circleci-parallelize --headless --chrome-binary-location=/usr/bin/google-chrome -vv --gherkin-terminal-reporter --junitxml=test_results/output.xml ./ui_tests/caseworker

caseworker-e2e-selenium-test-dbt-plafform:
	@echo "*** Requires starting the caseworker stack, which can be started running: 'make start-caseworker' ***"
	$(docker-e2e-caseworker-dbt-plafform) exec caseworker bash -c '$(wait-for-caseworker)' && PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest --circleci-parallelize --headless --chrome-binary-location=/usr/bin/google-chrome -vv --gherkin-terminal-reporter --junitxml=test_results/output.xml ./ui_tests/caseworker

exporter-e2e-selenium-test:
	@echo "*** Requires starting the exporter stack, which can be started running: 'make start-exporter' ***"
	$(docker-e2e-exporter) exec exporter bash -c '$(wait-for-exporter)' && PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest --circleci-parallelize --headless --chrome-binary-location=/usr/bin/google-chrome -vv --gherkin-terminal-reporter --junitxml=test_results/output.xml ./ui_tests/exporter

exporter-e2e-selenium-test-dbt-plafform:
	@echo "*** Requires starting the caseworker, which can be started running: 'make start-caseworker' ***"
	$(docker-e2e-exporter-dbt-plafform) exec caseworker bash -c '$(wait-for-caseworker)' && PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest --circleci-parallelize --headless --chrome-binary-location=/usr/bin/google-chrome -vv --gherkin-terminal-reporter --junitxml=test_results/output.xml ./ui_tests/caseworker

build-exporter:
	$(docker-e2e-exporter) build
