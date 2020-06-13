#!/usr/bin/env bash

if [[ "$TRAVIS_TAG" = "" ]]
then
    echo "Make gh-pages"
    node-sass helpers/gh_pages_content/style.scss helpers/gh_pages_content/style.css --output-style compressed
    html-minifier helpers/gh_pages_content/index.html --output helpers/gh_pages_content/index.html --html5 --remove-comments --remove-tag-whitespace --collapse-inline-tag-whitespace --remove-attribute-quotes --collapse-whitespace
    git add -A
    git commit -a -m upd
fi
