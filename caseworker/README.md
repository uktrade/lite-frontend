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
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run pytest
```

## Testing

### Unit tests
```
$ PIPENV_DOTENV_LOCATION=caseworker.env pipenv run ./manage.py runserver localhost:8200
```

### Browser tests

* Install Chromedriver
* Make sure that your .env file has the correct information:
  * `cd ui_automation_tests/local.env ui_automation_tests/.env` 
  * Fill in the fields you need for the .env
  * ENVIRONMENT = Whichever environment you want to run it against e.g local for local
  * TEST DATA - You will need certain data such as SSO users email and name. All of this information is accessible for Vault in the .env file for each project.
  * PORT = This needs to equal whichever port you are running your code locally. So if you are running your front end code on 9000, PORT should equal 9000.
  * LITE_API_URL = Same as above but for API.


## Related Repositories

* [lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.
* [lite-spire-archive](https://github.com/uktrade/lite-spire-archive) - Service for retrieving historic SPIRE data