# lite-internal-frontend

Application for handling internal information in LITE.

## Running the application

* Download the repository:
  * `git clone https://github.com/uktrade/lite-internal-frontend.git`
  * `cd lite-internal-frontend`
* Start a local Postgres: `docker run --name my-postgres -e POSTGRES_PASSWORD=password -p 5432:5432 -d postgres`
* Set up your local config file:
  * `cp local.env .env`
  * If you're not running Postgres with the default options, edit the `DATABASE_URL` sections of the `.env` file
* Initialise submodules:
  * `git submodule init`
  * `git submodule update`
* Setup Pipenv environment:
  * `pipenv sync`
* Run the application: `pipenv run ./manage.py migrate && pipenv run ./manage.py runserver 9000`
* Go to the index page (e.g. `http://localhost:9000`)

## Running selenium tests

* Setup chromedriver
  * `` CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` ``
  * `CHROME_DRIVER_FILENAME='chromedriver_mac64.zip'`
  * `curl -o ~/$CHROME_DRIVER_FILENAME http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/$CHROME_DRIVER_FILENAME`
  * `unzip ~/$CHROME_DRIVER_FILENAME -d ~/ && rm ~/$CHROME_DRIVER_FILENAME`
  * `sudo mv -f ~/chromedriver /usr/local/bin/chromedriver`
  * `sudo chown root:admin /usr/local/bin/chromedriver`
  * `sudo chmod 0755 /usr/local/bin/chromedriver`
* Setup dev pipenv environment:
  * `pipenv sync -d`
* Run `pipenv run python -m pytest`

## LITE Repositories

[lite-api](https://github.com/uktrade/lite-api) - Service for handling backend calls in LITE.

[lite-exporter-frontend](https://github.com/uktrade/lite-exporter-frontend) - Application for handling exporter related activity in LITE.

**[lite-internal-frontend](https://github.com/uktrade/lite-internal-frontend)** - Application for handling internal information in LITE.
