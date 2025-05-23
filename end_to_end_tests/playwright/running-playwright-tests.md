Using Playwright
----------------

[Playwright](https://playwright.dev/python/docs/intro) is a package to help write and run end to end tests.

### How to use playwright

Running `make playwright_run_tests` or `make playwright_run_tests_docker` will run the tests using environment variables in `end_to_end_tests/playwright/.env`

`end_to_end_tests/playwright/example.env` provides defaults for all required environment variables.

Create your own copy of the .env
```bash
cp end_to_end_tests/playwright/example.env end_to_end_tests/playwright/.env
```
Make sure the users with the email addresses specified exist on your local install.

### Prerequisites

The default demo organisation `Archway Communications` needs to exist and the exporter user needs to be an administrator of it.

1. Run `./manage.py seedexporterusers` on `lite-api` This will create the demo organisation and any exporter users specified in `EXPORTER_USERS` env var.
2. Run `./manage.py seedinternalusers` on `lite-api` This will create any internal users specified in `INTERNAL_USERS` env var.

The exporter email (user) specified in `end_to_end_tests/playwright/.env` needs to have been seeded.
The caseworker email (user) specified in `end_to_end_tests/playwright/.env` needs to have been seeded as a superuser.

The tests can only be run when Staff-SSO and GOV.UK One Login are disabled.

### Running, writing and debugging tests

The tests can be run locally or in a container.

To run with docker
```bash
docker compose build
make playwright_run_tests_docker
```

To run locally
```bash
make playwright_install
make playwright_run_tests
```

To debug a failing test the trace file will appear in the `test-results` folder.
```bash
make playwright_show_trace ARGUMENTS=test-results/<<path to trace.zip>>
```

To debug and actually see the tests being run in a browser (Note: playwright must be installed locally)
```bash
make playwright_run_tests_in_debug_mode
```

When adding a new test run one of the following commands.
The Playwright inspector will load up along with a browser at the correct login page.
Record your test by using the browser provided to run through your new test scenario .
The inspector will log all actions taken, asserts and expected urls can also be added during the generation of the test.
More information can be found here
[Generate playwright tests](https://playwright.dev/python/docs/codegen-intro)

To write a new a caseworker test
```bash
make playwright_write_caseworker_test
```

To write a new a exporter test
```bash
make playwright_write_exporter_test
```

An example approach of how to add a new test:

1. Copy the `test_example.py` for the application type you are testing
2. Rename TestExample class and test_example function to something appropriate.
3. Load the playwright codegen using one of the above commands
4. Record your test
5. Copy the generated test from Playwright inspector into new test file that you created in step 1 into either `def create_application` or `def manage_application`
6. Add `self.` to all `page` variables
7. Re-run your test and check it works on subsequent runs

### Troubleshooting

#### Unable to run the tests using docker

When using docker the container version needs to match the playwright package being installed
If there is a mismatch when attempting to run the tests the following message will appear.

```playwright._impl._errors.Error: BrowserType.launch: Executable doesn't exist at /ms-playwright/chromium_headless_shell-1169/chrome-linux/headless_shell
           ╔═══════════════════════════════════════════════════════════════╗
           ║ Looks like Playwright was just updated to 1.52.0.             ║
           ║ Please update docker image as well.                           ║
           ║ -  current: mcr.microsoft.com/playwright/python:v1.51.0-jammy ║
           ║ - required: mcr.microsoft.com/playwright/python:v1.52.0-jammy ║
           ║                                                               ║
           ║ <3 Playwright Team                                            ║
           ╚═══════════════════════════════════════════════════════════════╝
 ```
To fix the issue update `end_to_end_tests/playwright/docker/Dockerfile` and set the
 container version to that of the playwright version found in `Pipfile.lock`.
If these values already match then just rebuild your containers and re-run the tests.

#### F680 tests failing - Unable to find `Form 680 (F680) security approval` on apply for a licence page

This happens when the F680 feature has not been enabled.
1. On `lite-api` updated `.env` to include `FEATURE_FLAG_ALLOW_F680=True`
2. On `lite-frontend` updated `exporter.env` and `caseworker.env` to include `FEATURE_FLAG_ALLOW_F680=True``
3. Re-run the tests

#### Known issues

The tests currently run using firefox as there is an issue when testing the caseworker
screens with the application list view (landing page) when using chromium. The tests fail with the following error:
```
  56 × waiting for element to be visible, enabled and stable
       - element is visible, enabled and stable
       - scrolling into view if needed
       - done scrolling
       - <td class="govuk-table__cell">…</td> intercepts pointer events
     - retrying click action
       - waiting 500ms
```
If when running the tests or adding new tests and this error appears make sure `--browser firefox` is set.
