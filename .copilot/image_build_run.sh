#!/usr/bin/env bash

set -e

python ./manage.py collectstatic --ignore=*.scss,*.md,*.txt,*.json,LICENSE,license,CHANGES,changes