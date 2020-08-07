# lite-frontend

[![circle-ci-image]][circle-ci]

**Frontend for LITE - the Department for International Trade (DIT)**

---

## Development

### Requirements

* [Python 3.7](https://www.python.org/downloads/release/python-37/)
* [Postgres 10](https://www.postgresql.org/)
* [Redis](https://redis.io/)
* [Pipenv](https://pipenv.pypa.io/en/latest/)

### Installing 
    $ git clone https://github.com/uktrade/lite-frontend
    $ cd lite-frontend
    $ git submodule init
    $ git submodule update`
    $ pipenv install --dev

### Configuration

Secrets such as API keys and environment specific configurations are placed in `caseworker.env` and `exporter.env` - a file that is not added to version control. To create a template secrets file with dummy values run:

```
$ cp example.caseworker.env caseworker.env
$ cp example.exporter.env exporter.env
```

### Commands

To run code using the correct `caseworker` and `exporter` env var files you need to set the env var PIPENV_DOTENV_LOCATION to the desired location e.g.:


```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest
$ PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py runserver localhost:8300
$ PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest
```

## Helpful links
* [GDS service standards](https://www.gov.uk/service-manual/service-standard)
* [GDS design principles](https://www.gov.uk/design-principles)

## Related projects:
https://github.com/uktrade?q=lite
https://github.com/uktrade?q=spire

[circle-ci-image]: https://circleci.com/gh/uktrade/lite-frontend/tree/develop.svg?style=svg
[circle-ci]: https://circleci.com/gh/uktrade/lite-frontend/tree/develop
