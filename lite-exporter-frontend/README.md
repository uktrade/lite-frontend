# lite-exporter-frontend

[![CircleCI](https://circleci.com/gh/uktrade/lite-exporter-frontend.svg?style=svg)](https://circleci.com/gh/uktrade/lite-exporter-frontend)
[![Maintainability](https://api.codeclimate.com/v1/badges/07f341e7b8a40681c3c6/maintainability)](https://codeclimate.com/github/uktrade/lite-exporter-frontend/maintainability)

Application for handling exporter related activity in LITE.

## Running the service with docker
* Download the repository
  * `git clone https://github.com/uktrade/lite-exporter-frontend.git`
  * `cd lite-exporter-frontend`
* First time setup
  * Set up your local config file:
    * `cp docker.env .env`
  * Initialise submodules
    * `git submodule init`
    * `git submodule update`
  * Ensure docker is running
    * Build and start docker images:
    * `docker-compose build` - build the container image
    * `docker-compose up`  - to bring up the db and the api service to allow the migrate to succeed
  * Run the migrations
    * `./bin/migrate.sh` - Perform the Django migrations
* Starting the service
    * `docker-compose up`
* Stopping the service
    * `docker-compose stop`
* Tear down the service
    * `docker-compose down`
* Go to the index page (e.g. `http://localhost:8300`)
***

## Running the application

* Download the repository:
  * `git clone https://github.com/uktrade/lite-exporter-frontend.git`
  * `cd lite-exporter-frontend`
* Start a local Postgres: `docker run --name lite-frontend -e POSTGRES_PASSWORD=password -p 5430:5432 -d postgres`
* Set up your local config file:
  * `cp local.env .env`
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Initialise submodules
  * `git submodule init`
  * `git submodule update`
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 9000`
* Go to the index page (e.g. `http://localhost:9000`)


## Running selenium tests

### Installing
* Install Chromedriver
  * `brew cask install chromedriver`
* or via browser:
  * Download chromedriver from http://chromedriver.chromium.org/ and install it  
  * make sure it has execute permissions and is in PATH
* Setup dev pipenv environment:
  * `pipenv sync -d`
* Make sure that your .env file has the correct information
  * ENVIRONMENT = Whichever environment you want to run it against e.g local for local
  * TEST DATA - You will need certain data such as SSO users email and name. All of this information is accessible for Vault in the .env file for each project.
  * PORT = This needs to equal whichever port you are running your code locally. So if you are running your front end code on 9000, PORT should equal 9000.
  * LITE_API_URL = Same as above but for API.

### Running tests
* To run tests via command line, run `pipenv run python -m pytest` from within the `ui_automation_tests` folder.
* For a specific tag (don't include the @) `pipenv run python -m pytest -m "tag name"`
* To run in parallel `pipenv run python -m pytest -n 3 --dist=loadscope` (replace 3 with how many you want in parallel.)
* To ignore certain folders `pipenv run python -m pytest --ignore=some_folder`
* To automatically re run failed tests once(to try and avoid flaky UI tests)  add  `--reruns 1`

### Running tests via Pycharm tips
* You may need to make sure in pycharm, within Preferences -> Tools -> Python Integrated Tools -> Default Test Runner is pytest
* You may need to change the run configuration for the tests too. Click on run, edit configurations and make sure the Python framework being used in the left hand pane is Python tests 


## Running Bandit

`pipenv run bandit -r .`

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

**[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend)** - Application for handling exporter related activity in LITE.

[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend) - Application for handling internal information in LITE.
