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