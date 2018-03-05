#!/usr/bin/env bash

if [[ "$allow_deploy" = "true" ]]
then
echo "Deploy! ($TRAVIS_TEST_RESULT)"

cp helpers/.builder.py .
cp helpers/.providers_updater.py .
cp helpers/manga.spec .
python .providers_updater.py
lessc helpers/gh_pages_content/style.less helpers/gh_pages_content/style.css
html-minifier helpers/gh_pages_content/index.html --output helpers/gh_pages_content/index.html --html5 --remove-comments --remove-tag-whitespace --collapse-inline-tag-whitespace --remove-attribute-quotes --collapse-whitespace
html-minifier helpers/gh_pages_content/improvement.html --output helpers/gh_pages_content/improvement.html --html5 --remove-comments --remove-tag-whitespace --collapse-inline-tag-whitespace --remove-attribute-quotes --collapse-whitespace
git add -A
git commit -a -m upd

./cc-test-reporter after-build -t coverage.py --exit-code $TRAVIS_TEST_RESULT || true

if [[ "$TRAVIS_TAG" != "" ]]
then
echo "Start build bin package"
pyinstaller manga.spec --log-level CRITICAL -y -F
fi

fi
