#!/bin/sh -e

echo "Write new exporter test"
set -a
source playwright/.env
python -m playwright codegen $EXPORTER_URL --target python-pytest
exit
set +a
