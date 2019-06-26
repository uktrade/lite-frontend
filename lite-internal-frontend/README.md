# lite-internal-frontend

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
* Start a local Postgres: `docker run --name my-postgres -e POSTGRES_PASSWORD=password -p 5431:5432 -d postgres`
* `cp local.env .env` : Create a local environment configuration file, you will need to add tokens
  and keys the
* Set up your local config file:
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 8080`
* Go to the index page (e.g. `http://localhost:8080`)


## Running selenium tests
* Setup ChromeDriver:
  * `` CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` ``
  * `CHROME_DRIVER_FILENAME='chromedriver_mac64.zip'`
  * `curl -o ~/$CHROME_DRIVER_FILENAME http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/$CHROME_DRIVER_FILENAME`
  * `unzip ~/$CHROME_DRIVER_FILENAME -d ~/ && rm ~/$CHROME_DRIVER_FILENAME`
  * `sudo mv -f ~/chromedriver /usr/local/bin/chromedriver`
  * `sudo chown root:admin /usr/local/bin/chromedriver`
  * `sudo chmod 0755 /usr/local/bin/chromedriver`
* Setup developer Pipenv environment:
  * `pipenv sync -d`
* Run `pipenv run python -m pytest`
* You will need to change your .env file to include:
`TEST_SSO_EMAIL="email here"`
`TEST_SSO_PASSWORD="pw here"`
Ask someone on the team for valid credentials here.

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend) - Application for handling exporter related activity in LITE.

**[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend)** - Application for handling internal information in LITE.
