#!/bin/sh -e

echo "Running Playwright trace viewer"
python -m playwright show-trace $1
