#!/usr/bin/env bash

if [[ "$allow_deploy" = "true" ]]
then

    if [[ "$TRAVIS_TAG" != "" ]]
    then
        echo "Skip build bin package"
#        echo "Start build bin package"
#        cp helpers/.builder.py .
#        cp helpers/.providers_updater.py .
#        cp helpers/manga.spec .
#        python .providers_updater.py
#        pyinstaller manga.spec --log-level CRITICAL -y -F
    else
        echo "Make gh-pages"
        node-sass helpers/gh_pages_content/style.scss helpers/gh_pages_content/style.css --output-style compressed
        html-minifier helpers/gh_pages_content/index.html --output helpers/gh_pages_content/index.html --html5 --remove-comments --remove-tag-whitespace --collapse-inline-tag-whitespace --remove-attribute-quotes --collapse-whitespace
        html-minifier helpers/gh_pages_content/improvement.html --output helpers/gh_pages_content/improvement.html --html5 --remove-comments --remove-tag-whitespace --collapse-inline-tag-whitespace --remove-attribute-quotes --collapse-whitespace
        git add -A
        git commit -a -m upd
    fi

fi
