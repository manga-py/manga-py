#!/usr/bin/env bash

if [[ "$allow_deploy" = "true" ]]
then

    if [[ "$TRAVIS_TAG" != "" ]]
    then
        echo "Start build bin package"
        cp helpers/.builder.py .
        cp helpers/.providers_updater.py .
        cp helpers/manga.spec .
        python .providers_updater.py
        pyinstaller manga.spec --log-level CRITICAL -y -F
    fi

fi
