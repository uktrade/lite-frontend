#!/bin/sh -e

echo "Write new Caseworker test"
set -a
source playwright/.env
pipenv run python -m playwright codegen $CASEWORKER_URL --target python-pytest
set +a
