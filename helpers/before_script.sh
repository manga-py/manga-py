#!/usr/bin/env bash

cd ..

allow_deploy="false"

py_version=$(python --version)

if [[ "${py_version:7:-2}" = "3.5" ]]
then
allow_deploy="true"
fi
