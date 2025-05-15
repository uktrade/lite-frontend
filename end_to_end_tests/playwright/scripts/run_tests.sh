#!/bin/sh -e

echo "Running Playwright end to end tests"
pytest --tracing retain-on-failure --browser=firefox -c end_to_end_tests/playwright/docker/pytest.ini  end_to_end_tests/playwright/tests/ --numprocesses auto
