#!/bin/sh -e

echo "Write new Caseworker test"
set -a
source playwright/.env
python -m playwright codegen $CASEWORKER_URL --target python-pytest
set +a
