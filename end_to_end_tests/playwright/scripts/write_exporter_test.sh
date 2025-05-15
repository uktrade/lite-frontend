#!/bin/sh -e

echo "Write new exporter test"
set -a
source playwright/.env
pipenv run python -m playwright codegen $EXPORTER_URL --target python-pytest
exit
set +a
