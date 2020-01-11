#!/usr/bin/env bash

py_version=$(python --version)

if [[ "$TRAVIS_TAG" = "" ]]
then wget 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' -O /tmp/chrome.deb && sudo dpkg -i /tmp/chrome.deb && sudo apt-get install -y -f --fix-missing
fi
