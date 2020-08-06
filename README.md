# lite-frontend
Frontend for LITE


## Caseworker

### Runserver
```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200
```

### Unit tests

```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest
```

## Exporter

### Runserver

```
$ PIPENV_DOTENV_LOCATION=exporter.env pipenv run ./manage.py runserver localhost:8300
```

### Unit tests

```
$ PIPENV_DOTENV_LOCATION=exporter.env pipenv run pytest
```
