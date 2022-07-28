## E2E Tests

The aim of this test suite is perform end to end tests, simulating a user flow.

# e2e test Docker stack setup

End to end tests requires the following docker setup:

- Latest/Release Tagged API image (stored in GCR)
- Elasticsearch
- Redis
- Postgres DB using a UAT DB snapshot (stored in GCR)
- Caseworker/Exporter (built from code)

- Copy environment variables (make sure to save your current .env files before running the below):
```
cp ci.caseworker.env caseworker.env
cp ci.exporter.env exporter.env
cp ci.api.env api.env
```
- Fill the env files with appropriate values from Vault. Including vars with export statements.
  
```
# Common
export AUTHBROKER_CLIENT_ID=
export AUTHBROKER_CLIENT_SECRET=
export AWS_ACCESS_KEY_ID=
export AWS_REGION=
export AWS_SECRET_ACCESS_KEY=
export AWS_STORAGE_BUCKET_NAME=
export AUTH_USER_NAME=
export AUTH_USER_PASSWORD=
export BASIC_AUTH_ENABLED=
export ENDPOINT=
export TEST_SSO_EMAIL=
export TEST_SSO_PASSWORD=
export EXPORTER_TEST_SSO_EMAIL=
export EXPORTER_TEST_SSO_PASSWORD=

# Exporter specific
export EXPORTER_AUTHBROKER_URL=
export EXPORTER_AUTHBROKER_CLIENT_ID=
export EXPORTER_AUTHBROKER_CLIENT_SECRET=
export GOVUK_BASIC_AUTH_USER_NAME=
export GOVUK_BASIC_AUTH_USER_PASSWORD=
export BROWSER_HOSTS_EXPORTER=

# Caseworker specific
export DIRECTORY_SSO_API_CLIENT_BASE_URL=
export DIRECTORY_SSO_API_CLIENT_API_KEY=
export BROWSER_HOSTS_CASEWORKER=

# API specific
export AV_SERVICE_PASSWORD=
export AV_SERVICE_URL=
export AV_SERVICE_USERNAME=
```

### Caseworker Setup and run tests

- Open a terminal, source both api.env and caseworker.env. This will ensure all export statements are run and appropriate env vars are set and ready for docker-compose.
- run `make start-caseworker`
- Wait for it to start up. Open another terminal and run `make caseworker-e2e-selenium-test`

### Exporter Setup and run tests

- Open a terminal, source both api.env and exporter.env. This will ensure env vars are ready for docker-compose.
- run `make start-exporter`
- Wait for it to start up. Open another terminal and run `make exporter-e2e-selenium-test`
