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

# Caseworker specific
export DIRECTORY_SSO_API_CLIENT_BASE_URL=
export DIRECTORY_SSO_API_CLIENT_API_KEY=

# API specific
export AV_SERVICE_PASSWORD=
export AV_SERVICE_URL=
export AV_SERVICE_USERNAME=

# To Run Tests using the Mock SS0 in caseworker.env set
AUTHBROKER_URL=http://caseworker:8200
MOCK_SSO_ACTIVATE_ENDPOINTS=True
MOCK_SSO_USER_EMAIL=fake@fake.com (this user will need to be seeded as an internal user)
MOCK_SSO_USER_FIRST_NAME=LITE
MOCK_SSO_USER_LAST_NAME=Testing

```

### Caseworker Setup and run tests locally

- Open a terminal, source both api.env and caseworker.env. This will ensure all export statements are run and appropriate env vars are set and ready for docker-compose.
- run `make start-caseworker`
- Wait for it to start up. Open another terminal and run `make caseworker-e2e-selenium-test`

### Setting up mock sso locally
- add 127.0.0.1 caseworker to your hosts file
- using API commands seedinternaluser  test-uat-user@digital.trade.gov.uk

### Exporter Setup and run tests locally

- Open a terminal, source both api.env and exporter.env. This will ensure env vars are ready for docker-compose.
- run `make start-exporter`
- Wait for it to start up. Open another terminal and run `make exporter-e2e-selenium-test`


### Running automated tests before production release
Jenkins job `lite-frontend-ui-tests` is designed to run both caseworker and exporter tests on demand for specific release tags or branches.

First step is to make sure the `lite-api` image is tagged correctly in GCR. A GCR trigger builds image upon preparing git release. But, until fixed, it won't be tagging that image with correct release tag. This must be done manually using GCR console. As soon as git release process is done on Github, head to triggered builds [here](https://console.cloud.google.com/gcr/images/sre-docker-registry/global/github.com/uktrade/lite-api). And tag the latest built image with the release tag (v1.34.0 for ex).

Once tagging is done, open Jenkins [job](https://jenkins.ci.uktrade.digital/view/LITE/job/lite-frontend-ui-tests/) >> Build with parameters >> select correct release tag for FE and API as you would do with UAT/Production release >> let it run the tests. You can see the tests running [here](https://app.circleci.com/pipelines/github/uktrade/lite-frontend?filter=all) in CircleCI.
