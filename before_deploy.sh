#!/usr/bin/env bash

allow_deploy="false"

c=$(which python | wc -l)
if [ c -ge 1 ]
  then
    py_version=$(python --version)

    if [[ "${py_version:7:-2}" = "3.6" ]]
      then
        allow_deploy="true"
      else
        echo "${py_version:7:-2}"
    fi
fi