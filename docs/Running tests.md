## E2E Tests

The aim of this test suite is perform end to end tests, simulating a user flow.

### Setup

Pre-requisites:

Ensure you have [node](https://nodejs.org/en/download/) v14 installed then install dependencies:

`$ npm install`

Ensure `caseworker.env` is present and has the required `CYPRESS` environment variables present.

### Running the tests

The e2e test suite is triggered by running the following command:

`$ npm run test:e2e`

### Running the tests manually in cypress interface

`$ npm run test:e2e:watch`

### Running a specific spec

`$ npm run test:e2e:dit -- --spec test/integration/caseworker/organisation.spec.js`
