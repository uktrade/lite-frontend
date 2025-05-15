#!/bin/sh -e

echo "Write new exporter test"
set -a
source end_to_end_tests/playwright/.env
python -m playwright codegen $EXPORTER_URL --target python-pytest --browser firefox
set +a
