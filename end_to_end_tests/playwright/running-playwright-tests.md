Using Playwright
----------------

Running `make playwright_run_tests` or `make playwright_run_tests_docker` will run the tests using environment variables in `end_to_end_tests/playwright/.env`

`end_to_end_tests/playwright/example.env` provides defaults for all required environment variables.

The tests can only be run when Staff-SSO and GOV.UK One Login are disabled.

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
