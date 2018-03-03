#!/usr/bin/env bash

allow_deploy="false"

py_version=$(python --version)

if [[ "${py_version:7:-2}" = "3.6" ]]
  then
    echo "Deploy! ($TRAVIS_TEST_RESULT)"
    ALLOW_DEPLOY="true"
    ./cc-test-reporter after-build -t coverage.py --exit-code $TRAVIS_TEST_RESULT || true
    if [[ "$TRAVIS_TAG" != "" ]]; then
        echo "Start build bin package"
        pyinstaller manga.spec --log-level CRITICAL -y -F
    fi
fi
