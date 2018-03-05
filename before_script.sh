#!/usr/bin/env bash

allow_deploy="false"

py_version=$(python --version)

if [[ "${py_version:7:-2}" = "3.6" ]]
then
allow_deploy="true"
fi
