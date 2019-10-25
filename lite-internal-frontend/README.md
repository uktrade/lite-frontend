# lite-internal-frontend

[![CircleCI](https://circleci.com/gh/uktrade/lite-internal-frontend.svg?style=svg)](https://circleci.com/gh/uktrade/lite-internal-frontend)
[![Maintainability](https://api.codeclimate.com/v1/badges/d981279d8fd1fdd2d96c/maintainability)](https://codeclimate.com/github/uktrade/lite-internal-frontend/maintainability)

Application for handling internal information in LITE.

## Download and setup the project:
  * `git clone https://github.com/uktrade/lite-internal-frontend.git`
  * `cd lite-internal-frontend`
  * `git submodule init`
  * `git submodule update`


## Running this web service using Docker
Using docker isolates the service and development environment from
that installed on the local host (dev machine). Recreating this environment in docker is both
deterministic and reliable.


### Initial setup
 * `cp docker.env .env` : Create a local environment configuration file, you will need to add tokens
  and keys the
Here the migrations need to be run before the service is used for the fist time and every time the service is torn down
  * `docker-compose build` : Build the docker image, this may take a little while the very first time.
 After that it will be much faster as the container layers are cached locally.
  * `./bin/migrate.sh` : Run migrations to setup the database.


### Managing the service
* `docker-compose up` : Starting the service
* `docker-compose stop` : Stopping the service
* `docker-compose down` : Tearing down the service, this clears the database.
Note the migrations will need to be run again the next time the service is to be used


### Using the service
* Ensure that the [lite-api](https://github.com/uktrade/lite-api) service is running
* Ensure this service is initialised and running
* Go to the index page (e.g. `http://localhost:8200`)


## Running the application locally on your dev machine not using Docker
* Start a local Postgres: `docker run --name lite-internal-frontend -e POSTGRES_PASSWORD=password -p 5431:5432 -d postgres`
* Mock S3: `docker run -p 9090:9090 -p 9191:9191 -t adobe/s3mock`
* `cp local.env .env` : Create a local environment configuration file, you will need to add tokens
  and keys the
* Set up your local config file:
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 8080`
* Go to the index page (e.g. `http://localhost:8080`)


## Running selenium tests
* Setup chromedriver
  * Download chromedriver from http://chromedriver.chromium.org/ and install it  
  * make sure it has execute permissions and is in PATH
* or
  * `brew cask install chromedriver`

* Setup dev pipenv environment:
  * `pipenv sync -d`
* Run `pipenv run python -m pytest`
* For a specific tag (don't include the @) `pipenv run python -m pytest -m "tag name"`
* To run in parallel `pipenv run python -m pytest -n 3` (replace 3 with how many you want in parallel.)
* You may need to make sure in pycharm, within Preferences -> Tools -> Python Integrated Tools -> Default Test Runner is pytest
* You may need to change the run configuration for the tests too. Click on run, edit configurations and make sure the Python framework being used in the left hand pane is Python tests 
* You will need to change your .env file to include:
`TEST_SSO_EMAIL="email here"`
`TEST_SSO_PASSWORD="pw here"`
`TEST_SSO_NAME="name here"`

Ask someone on the team for valid credentials here.


## Running Bandit

`pipenv run bandit -r .`


## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend) - Application for handling exporter related activity in LITE.

**[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend)** - Application for handling internal information in LITE.
