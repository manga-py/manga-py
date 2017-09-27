#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangadoom.co'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('ul.chapter-list > li > a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.co/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = re.search(' images = (\[{[^;]+}\])', content)
    if not items:
        return []
    try:
        images = json.loads(items.groups()[0])
        return [i['url'] for i in images]
    except json.JSONDecodeError:
        return []


def get_manga_name(url, get=None):
    name = re.search('\\.co/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
