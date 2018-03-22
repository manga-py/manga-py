#!/usr/bin/env bash

allow_deploy="false"

py_version=$(python --version)

if [[ "${py_version:7:-2}" = "3.5" ]]
then
allow_deploy="true"
fi
if [[ "$TRAVIS_TAG" = "" ]]
then wget 'https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb' -O /tmp/chrome.deb && sudo dpkg -i /tmp/chrome.deb && sudo apt-get install -y -f --fix-missing
fi
