# lite-exporter-frontend

Application for handling exporter related activity in LITE.


## Running the service with docker
* Download the repository
  * `git clone https://github.com/uktrade/lite-exporter-frontend.git`
  * `cd lite-exporter-frontend`
* First time setup
  * Set up your local config file:
    * `cp local.env .env`
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
* Go to the index page (e.g. `http://localhost:8110`)
***

## Running the application

* Download the repository:
  * `git clone https://github.com/uktrade/lite-exporter-frontend.git`
  * `cd lite-exporter-frontend`
* Start a local Postgres: `docker run --name lite-frontend -e POSTGRES_PASSWORD=password -p 5430:5432 -d postgres`
* Set up your local config file:
  * `cp sample.env .env`
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Initialise submodules
  * `git submodule init`
  * `git submodule update`
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 9000`
* Go to the index page (e.g. `http://localhost:9000`)

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

**[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend)** - Application for handling exporter related activity in LITE.

[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend) - Application for handling internal information in LITE.
