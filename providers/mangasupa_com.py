#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://mangasupa.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.chapter-list .row a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('/chapter/[^/]+/([^/]+)', volume)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    items = document_fromstring(get(volume)).cssselect('.vung_doc img')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    name = re.search('\\.com/(?:manga|chapter)/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
