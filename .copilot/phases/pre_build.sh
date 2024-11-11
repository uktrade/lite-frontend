#!/usr/bin/env bash

set -e

sed -i '15 s/build_exporter/build_exporter_dbt/' package.json
sed -i '15 s/build_caseworker/build_caseworker_dbt/' package.json
