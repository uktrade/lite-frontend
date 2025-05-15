#!/bin/sh -e

echo "Running Playwright trace viewer"
pipenv run python -m playwright show-trace $1
