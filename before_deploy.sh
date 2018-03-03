#!/usr/bin/env bash

allow_deploy="false"

py_version=$(python --version)

if [[ "$ALLOW_DEPLOY" = "true" ]]
  then
    if [[ "$TRAVIS_TAG" != "" ]]; then
        echo "Start build bin package"
        pyinstaller manga.spec --log-level CRITICAL -y -F
    fi
fi
