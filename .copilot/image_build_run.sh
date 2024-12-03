#!/usr/bin/env bash

set -e

export DJANGO_SECRET_KEY="example"
export TOKEN_SESSION_KEY="example"
export AUTHBROKER_URL="example"
export AUTHBROKER_CLIENT_ID="example"
export AUTHBROKER_CLIENT_SECRET="example"
export AWS_STORAGE_BUCKET_NAME="example"
export LITE_API_URL="example"
export PERMISSIONS_FINDER_URL="example"
export NOTIFY_FEEDBACK_TEMPLATE_ID="example"
export NOTIFY_FEEDBACK_EMAIL="example"
export FEEDBACK_URL="example"
export INTERNAL_FRONTEND_URL="example"
export LITE_EXPORTER_HAWK_KEY="example"
export COPILOT_ENVIRONMENT_NAME="example"
export LITE_INTERNAL_HAWK_KEY="example"

declare -a settings_modules=(conf.exporter conf.caseworker)

for setting_module in "${settings_modules[@]}"; do
  export DJANGO_SETTINGS_MODULE=$setting_module
  python manage.py collectstatic --ignore=*.scss,*.md,*.txt,*.json,LICENSE,license,CHANGES,changes
done