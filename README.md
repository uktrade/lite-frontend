# lite-frontend

[![circle-ci-image]][circle-ci]
[![coverage-image]][coverage]

**Frontend for LITE - the Department for International Trade (DIT)**

---

## Development

### Requirements

- [Python 3.9](https://www.python.org/downloads/release/python-39/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

### Installing

    $ git clone https://github.com/uktrade/lite-frontend
    $ cd lite-frontend
    $ git submodule init
    $ git submodule update
    $ pipenv install --dev

#### Git pre-commit setup

- Install pre-commit (see instructions here: https://pre-commit.com/#install)
- Run `pre-commit install` to activate pre-commit locally
- Run following to scan all files for issues
  - `pre-commit run --all-files`
- After this initial setup, pre-commit should run automatically whenever you run `git commit` locally.
- All developers must use the pre-commit hooks for the project. This is to make routine tasks easier (e.g. linting, style checking) and to help ensure secrets and personally identifiable information (PII) are not leaked.
- You should be able to use the project python environment to run pre-commit, but if the project python does not work for you, you should find a workaround for your dev environment (e.g. running a different higher python version just for pre-commit) or raise it with other developers. **Ignoring pre-commit errors is not an option.**
- This Repo is private and not avilable for public viewing due to sensitive material.

### Configuration

Secrets such as API keys and environment specific configurations are placed in `caseworker.env` and `exporter.env` - a file that is not added to version control. To create a template secrets file with dummy values run:

```
make secrets
```

### Commands

To run the webserver for caseworker and exporter use these commands:

```
make run_caseworker
make run_exporter
```

### Running with Docker

- Download the repository:

  - `git clone https://github.com/uktrade/lite-frontend.git`
  - `cd lite-frontend`

#### First time setup

- Set up your local config file:
  - `make secrets`
  - populate the newly created `caseworker.env` and `exporter.env` with values from Vault.

* Ensure docker is running

* Build and start docker images:
  - If you haven't already done this for lite-api, set up a shared docker network:
    - `docker network create lite` - shared network to allow API and frontend to communicate
  - `docker-compose build` - build the container image
* Installation requirements
  - install libmagic

#### Starting the service

- `docker-compose up -d` - to start the two frontend Django servers

- Ensure you have a working version of `lite-api` running, see [the instructions for running it
  in docker](https://github.com/uktrade/lite-api/blob/master/README.md#running-the-service-with-docker)

- Visit:
  - [http://localhost:8200](http://localhost:8200) for the caseworker frontend
  - [http://localhost:8300](http://localhost:8300) for the exporter frontend

#### Running unit tests

To run unit tests:

```
make run_unit_tests_caseworker
make run_unit_tests_exporter
make run_unit_tests_core
make run_all_unit_tests
```

## Helpful links

- [GDS service standards](https://www.gov.uk/service-manual/service-standard)
- [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:

https://github.com/uktrade?q=lite
https://github.com/uktrade?q=spire

[circle-ci-image]: https://circleci.com/gh/uktrade/lite-frontend/tree/master.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/lite-frontend/tree/master
[coverage-image]: https://api.codeclimate.com/v1/badges/7bb724ad7dc3c9be3733/test_coverage
[coverage]: https://codeclimate.com/github/uktrade/lite-frontend/test_coverage

## Mock SSO

Currently we have Mock SSO enabled by default. You should be able to use Mock SSO in your own env files without changing any of the defaults provided in `example.caseworker.env` or `example.exporter.env`.

Previously you had to set the Mock SSO email in an env variable `MOCK_SSO_USER_EMAIL` in `caseworker.env` for this to work. Now this is optional as there is an input box which allows you to type in an email you want to use for Mock SSO. This change was made because having the input box is useful for running tests using CI.

## UI tests

We use pytest + Selenium for end-to-end tests.

Run all tests

```
PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest ui_tests/
make run_ui_tests
```

Run all Unit and UI tests

```
make run_all_tests
```

> You can use the flags `--step-through` (in conjunction with `-s`) and `--step-verbose` to stop on each step. Helpful for exploration and debugging.

> The UI tests (a.k.a. end-to-end tests, e2e tests, browser tests or functional tests) require some local configuration
> changes before they can run. As mentioned above, you need to run `make run_caseworker` and `make run_exporter`.
> These copy the `example.caseworker.env` and `example.exporter.env` files to `caseworker.env` and `exporter.env`
> respectively. In each file, the following variables need to have different values (see development team members for
> what those values should be or just try looking in Vault):

- AUTHBROKER_CLIENT_ID
- AUTHBROKER_CLIENT_SECRET
- AUTHBROKER_URL - should be https://sso.trade.uat.uktrade.io for caseworker but https://great.uat.uktrade.digital
  for the exporter
- AWS_ACCESS_KEY_ID
- AWS_SECRET_ACCESS_KEY
- AWS_STORAGE_BUCKET_NAME
- AWS_REGION
- TEST_SSO_EMAIL
- TEST_SSO_PASSWORD
- TEST_SSO_NAME (for the caseworker)
- NOTIFY_KEY
- NOTIFY_FEEDBACK_TEMPLATE_ID
- NOTIFY_FEEDBACK_EMAIL
- ENVIRONMENT - set to "local" if the tests are targeting the local caseworker
  and exporter. If not set the UI tests will try talking to devdata
- DIRECTORY_SSO_API_CLIENT_BASE_URL - Needed by the UI tests but not the caseworker or exporter, available
  in Vault
- DIRECTORY_SSO_API_CLIENT_API_KEY - Needed by the UI tests but not the caseworker or exporter, available
  in Vault

Exporter UI Tests also requires the following :

- GOVUK_BASIC_AUTH_USER_NAME - In vault used for GOV.UK basic authentication in test envs  
- GOVUK_BASIC_AUTH_USER_PASSWORD - In vault used for GOV.UK basic authentication in test envs
- EXPORTER_TEST_SSO_EMAIL - In vault this is a default account setup for testing
- EXPORTER_TEST_SSO_PASSWORD - In vault this is a default account setup for testing
- EXPORTER_TEST_SSO_NAME=LITE Testing

Before running the UI tests, make sure you have the following services running with corresponding ports:

- lite-api (port=**8100**)
- casework (port=**8200**)
- exporter (port=**8300**)

An example for how to run the above service:

```bash
cd lite-api
PIPENV_DOTENV_LOCATION=.env pipenv run python ./manage.py runserver 8100
cd ../lite-frontend
PIPENV_DOTENV_LOCATION=caseworker.env pipenv run python ./manage.py runserver 8200
PIPENV_DOTENV_LOCATION=exporter.env pipenv run python ./manage.py runserver 8300
```

You will also need to seed the lite-api database with the TEST_SSO_EMAIL (as well as running **seedall**
command - see https://github.com/uktrade/lite-api). If the email was `fake@fake.com` the
command would be (run against the lite-api virtual environment):

```bash
INTERNAL_USERS='[{"email"=>"fake@fake.com"}]' ./manage.py seedinternalusers
```

Finally, to run a UI test on the command line (will run an exporter and caseworker test tagged with `@run_this_test`):

```bash
PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -m "run_this_test" ui_tests/exporter
PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -m "run_this_test" ui_tests/caseworker/
```
## Ui Tests with Docker
All env variables above apply

Assuming you already have an instance of the api and frontend running using docker-compose you can either:

Run the tests from the frontend directory:
```
make run_docker_ui_tests
```

to do this manually:
```
docker-compose exec caseworker bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}"
docker-compose exec exporter bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}"
```

Connect to the box and run the tests:
**caseworker**
```
docker-compose exec caseworker bash
pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
```
**exporter**
```
docker-compose exec exporter bash
pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter ${ADDITIONAL_PYTEST_UI_TEST_ARGS}
```

${ADDITIONAL_PYTEST_UI_TEST_ARGS} is always set to --headless in the docker-compose so if you'd like to run without headless simply run:

```
pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker
pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter
```
or
```
docker-compose exec caseworker bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/caseworker"
docker-compose exec exporter bash -c "pytest -vv --gherkin-terminal-reporter ./ui_tests/exporter"
```

## Javascript/SCSS

The Javascript/SCSS is automatically watched via the node docker service.

The production assets are built on deployment as part of the cloudfoundry build. We specify the [node buildpack in the cloudfoundry manifest file](./manifest.yml#L4) which cloudfoundry automatically picks up. This then runs the command specified [`heroku-postbuild` specified in the package.json](./package.json#L14).

to run the tests run:
`docker exec -it lite-frontend_frontend_assets_watcher_1 npm run test`

### Without docker

Node version required can be found in the `package.json` under `engines`.
All javascripts and scss files are stored under caseworker/assets and exporter/assets

```
  npm i
```

Hot reload for local development.

```
  npm run watch
```
