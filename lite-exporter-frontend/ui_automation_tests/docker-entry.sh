#!/usr/bin/env bash

set -x

# run py.test ($@ to derive parameters from commandline)
if [ $NO_OF_PARALLEL_RUNNERS -gt 1 ]
then
    py.test -k "$TESTS_TO_RUN" -n="$NO_OF_PARALLEL_RUNNERS" --dist=loadscope  --reruns 1 --ignore=core --alluredir=ui_automation_tests/allure-results &
else
    py.test -k "$TESTS_TO_RUN"  --reruns 1 --ignore=core --alluredir=ui_automation_tests/allure-results &
fi
pid="$!"

# trap process id to stop script using Control+C
trap "echo '=== Stopping PID $pid ==='; kill -SIGTERM $pid" SIGINT SIGTERM

wait $pid
