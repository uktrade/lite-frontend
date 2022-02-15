# lite-frontend caseworker

**Application for handling internal information in LITE.**

---

## Development

Note this README is supplementary to the project root's README.

### Requirements
Additional to the requirements listed in the project root's README, you also need:

* Ensure that the [lite-api](https://github.com/uktrade/lite-api) service is running on port 8100
* Mock S3: `docker run -p 9090:9090 -p 9191:9191 -t adobe/s3mock`

### Runserver

To run code using the correct env var files you need to set the env var PIPENV_DOTENV_LOCATION to the desired location e.g.:


```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py migrate
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200
```

## Testing

### Unit tests
```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest unit_tests/caseworker
```

### Browser tests
```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest ui_tests/caseworker
```


## Related Repositories

* [lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.
* [lite-spire-archive](https://github.com/uktrade/lite-spire-archive) - Service for retrieving historic SPIRE data
