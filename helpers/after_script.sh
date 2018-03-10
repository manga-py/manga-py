#!/usr/bin/env bash

if [[ "$allow_deploy" = "true" ]]
then
    coverage xml
    ./cc-test-reporter after-build -t coverage.py --exit-code $TRAVIS_TEST_RESULT || true
fi
