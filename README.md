# lite-frontend

[![circle-ci-image]][circle-ci]
[![coverage-image]][coverage]


**Frontend for LITE - the Department for International Trade (DIT)**

---

## Development

### Requirements

- [Python 3.7](https://www.python.org/downloads/release/python-37/)
- [Pipenv](https://pipenv.pypa.io/en/latest/)

### Installing

    $ git clone https://github.com/uktrade/lite-frontend
    $ cd lite-frontend
    $ git submodule init
    $ git submodule update
    $ pipenv install --dev

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
    - `cp example.exporter.env caseworker.env` - you will want to set this up with valid values, ask another developer or get them from Vault.
    - `cp example.caseworker.env exporter.env` - you will want to set this up with valid values, ask another developer or get them from Vault.

  * Ensure docker is running

  * Build and start docker images:
    - If you haven't already done this for lite-api, set up a shared docker network:
      - `docker network create lite` - shared network to allow API and frontend to communicate
    - `docker-compose build` - build the container image

#### Starting the service
- `docker-compose up` - to start the two frontend Django servers

- Ensure you have a working version of `lite-api` running, see [the instructions for running it
  in docker](https://github.com/uktrade/lite-api/blob/master/README.md#running-the-service-with-docker)

- Visit:
    - [http://localhost:8200](http://localhost:8200) for the caseworker frontend
    - [http://localhost:8300](http://localhost:8300) for the exporter frontend

#### Running unit tests

To run unit tests:

```
make run_unit_tests
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

## UI tests

The UI tests (a.k.a. end-to-end tests, e2e tests, browser tests or functional tests) require some local configuration
changes before they can run. As mentioned above, you need to run `make run_caseworker` and `make run_exporter`.
These copy the `example.caseworker.env` and `example.exporter.env` files to `caseworker.env` and `exporter.env`
respectively. In each file, the following variables need to have different values (see development team members for
what those values should be or just try looking in lite-internal-frontend/devdata or 
lite-exporter-frontend/devdata in Vault):

* AUTHBROKER_CLIENT_ID 
* AUTHBROKER_CLIENT_SECRET
* AUTHBROKER_URL - should be https://sso.trade.uat.uktrade.io for caseworker but https://great.uat.uktrade.digital
  for the exporter
* AWS_ACCESS_KEY_ID
* AWS_SECRET_ACCESS_KEY
* AWS_STORAGE_BUCKET_NAM
* AWS_REGION
* TEST_SSO_EMAIL
* TEST_SSO_PASSWORD
* TEST_SSO_NAME (for the caseworker)
* DIRECTORY_SSO_API_CLIENT_BASE_URL - needed by the tests but not the frontend itself. Should be https://directory-sso-uat.london.cloudapps.digital
* DIRECTORY_SSO_API_CLIENT_API_KEY
* NOTIFY_KEY
* NOTIFY_FEEDBACK_TEMPLATE_ID
* NOTIFY_FEEDBACK_EMAIL
* ENVIRONMENT - set to "local" if the tests are targeting the local caseworker 
  and exporter. If not set the UI tests will try talking to devdata
* DIRECTORY_SSO_API_CLIENT_BASE_URL - Needed by the UI tests but not the caseworker or exporter,
  should be "https://directory-sso-uat.london.cloudapps.digital"
* DIRECTORY_SSO_API_CLIENT_API_KEY - Needed by the UI tests but not the caseworker or exporter, available
  in https://vault.ci.uktrade.digital/ui/vault/secrets/dit%2Flite/list/lite-internal-frontend/ui_automation_tests/

Before running the UI tests, make sure you have the following services running with corresponding ports:

* lite-api (port=**8100**)
* casework (port=**8200**)
* exporter (port=**8300**)

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

Finally, to run a UI test on the command line (will run an exporter and caseworker test tagged with `@login_test`):

```bash
PIPENV_DOTENV_LOCATION=exporter.env ENVIRONMENT=local pipenv run pytest -m "login_test" ui_tests/exporter
PIPENV_DOTENV_LOCATION=caseworker.env ENVIRONMENT=local pipenv run pytest -m "review_test" ui_tests/caseworker/
```