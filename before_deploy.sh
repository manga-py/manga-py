#!/usr/bin/env bash

if [[ "$allow_deploy" = "true" ]]
then
echo "Deploy! ($TRAVIS_TEST_RESULT)"

coverage xml
./cc-test-reporter after-build -t coverage.py --exit-code $TRAVIS_TEST_RESULT || true

if [[ "$TRAVIS_TAG" != "" ]]
then
echo "Start build bin package"
pyinstaller manga.spec --log-level CRITICAL -y -F
fi

fi
