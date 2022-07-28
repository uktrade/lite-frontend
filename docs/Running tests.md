## E2E Tests

The aim of this test suite is perform end to end tests, simulating a user flow.

### Caseworker Setup

To run the tests against the local docker stack ensure you follow the steps in [Running the stack](./Docker.md) before moving to the next steps.

After starting docker stack, make sure to update the below `caseworker.env` values from vault:

```
LITE_API_URL=http://localhost:8100
AUTHBROKER_CLIENT_ID=ValueInVault
AUTHBROKER_CLIENT_SECRET=ValueInVault
DIRECTORY_SSO_API_CLIENT_BASE_URL=ValueInVault
DIRECTORY_SSO_API_CLIENT_API_KEY=ValueInVault
BROWSER_HOSTS=<BROWSER_HOSTS_CASEWORKER>
```

### Running caseworker tests

You can run the tests by running the following make command after the docker stack is started:


`make caseworker-e2e-selenium-test`


### Exporter Setup

To run the tests against the local docker stack ensure you follow the steps in [Running the stack](./Docker.md) before moving to the next steps.

After starting docker stack, make sure to update the below `exporter.env` values from vault:

```
LITE_API_URL=http://localhost:8100
AUTHBROKER_URL=<EXPORTER_AUTHBROKER_URL>
AUTHBROKER_CLIENT_ID=<EXPORTER_AUTHBROKER_CLIENT_ID>
AUTHBROKER_CLIENT_SECRET=<EXPORTER_AUTHBROKER_CLIENT_SECRET>
BROWSER_HOSTS=<BROWSER_HOSTS_EXPORTER>
GOVUK_BASIC_AUTH_USER_NAME=ValueInVault
GOVUK_BASIC_AUTH_USER_PASSWORD=ValueInVault
TEST_SSO_EMAIL=<EXPORTER_TEST_SSO_EMAIL>
TEST_SSO_PASSWORD=<EXPORTER_TEST_SSO_PASSWORD>
```

### Running exporter tests

You can run the tests by running the following make command after the docker stack is started:


`make exporter-e2e-selenium-test`
