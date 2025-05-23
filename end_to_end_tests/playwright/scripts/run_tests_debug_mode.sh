#!/bin/sh -e

echo "Running Playwright end to end tests in debug mode"
echo "add page.pause() to test to set a break point"
PWDEBUG=1 pytest -v -s --tracing on -c end_to_end_tests/playwright/pytest.ini  end_to_end_tests/playwright/tests/ --numprocesses=auto $1

echo "Trace files can be found in test-results folder trace.zip"
