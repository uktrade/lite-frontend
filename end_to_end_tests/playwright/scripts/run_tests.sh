#!/bin/sh -e

echo "Running Playwright end to end tests"
pytest -v --tracing retain-on-failure -c end_to_end_tests/playwright/pytest.ini  end_to_end_tests/playwright/tests/ --numprocesses auto
