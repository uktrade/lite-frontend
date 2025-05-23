#!/bin/sh -e

echo "Write new Caseworker test"
set -a
source end_to_end_tests/playwright/.env
python -m playwright codegen $CASEWORKER_URL --target python-pytest --browser firefox
set +a
