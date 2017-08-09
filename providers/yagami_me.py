#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
# http://read.yagami.me/series/kubera/

domainUri = 'http://read.yagami.me'
uriRegex = 'https?://read\.yagami\.me/(?:series|read)/([^/]+)/?'

def test_url(url):
    test = re.match(uriRegex, url)
    if test is None:
        return False
    return len(test.groups()) > 0


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/series/{}'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None):
    parser = document_fromstring(content)
    result = parser.cssselect('#midside .list .element .title a')
    if result is None:
        return []
    return [i.get('href') for i in result]


def get_archive_name(volume, index: int = None):
    result = re.search('/read/.+?/(\d+/\d+)/', volume)
    return result.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    result = re.search('pages\s?=\s?(\[\{.+\}\])', content)
    if result is None:
        return []
    result = json.loads(result.groups()[0])
    return [i['url'] for i in result]


def get_manga_name(url, get=None):
    result = re.match(uriRegex, url).groups()
    return result[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
