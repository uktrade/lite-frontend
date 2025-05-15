Using Playwright
----------------

Running `make playwright_run_tests` or `make playwright_run_tests_docker` will run the tests using environment variables in `end_to_end_tests/playwright/.env`

`end_to_end_tests/playwright/example.env` provides defaults for all required environment variables.


The tests can only be run when Staff-SSO and GOV.UK One Login are disabled.


The tests can be run locally or in a container.
```bash
make playwright_run_tests
```

To run Playwright locally follow the following commands (this is for running the tests and test generation):
```bash
# Activate a venv before doing this
pip install --upgrade pip
pip install pytest-playwright
playwright install chromium
```
