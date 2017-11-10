#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://tapas.io'

def get_main_content(url, get=None, post=None):
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    items = re.search('episodeList\s?:\s?(\[{.+?}\])', content)
    if not items:
        return []
    items = [i['id'] for i in json.loads(items.groups()[0])]
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    return '{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    uri = '{}/episode/view/{}'.format(domainUri, volume)
    content = json.loads(get(uri))
    items = document_fromstring(content['data']['html']).cssselect('img.art-image')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    test = re.search('\\.io/(episode|series)/([^/]+)', url)
    if not test:
        raise UrlParseError()
    test = test.groups()
    if test[0] == 'series':
        return test[1]
    return document_fromstring(get(url))\
        .cssselect('span.tag')[0]\
        .text_content()\
        .strip('\n\t ')
