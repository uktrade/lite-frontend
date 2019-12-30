#!/usr/bin/env bash

set -x

# run py.test ($@ to derive parameters from commandline)
if [ -n "$TESTS_TO_RUN" ]
then
    py.test -k "$TESTS_TO_RUN"  --reruns 1 --ignore=core --disable-pytest-warnings --alluredir=ui_automation_tests/allure-results
else
    py.test -k "smoke"  --reruns 1 --ignore=core --disable-pytest-warnings --alluredir=ui_automation_tests/allure-results
    if [ $? -eq 0 ]
    then
        py.test -k "regression"  --reruns 1 --ignore=core --disable-pytest-warnings --alluredir=ui_automation_tests/allure-results
    fi
fi
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
