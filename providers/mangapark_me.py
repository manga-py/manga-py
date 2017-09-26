#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://mangapark.me'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('#list > div:last-child em a:last-child')
    if not parser:
        return []
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('/manga/[^/]+/([^/]+/[^/]+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0].replace('/', '_')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = document_fromstring(content).cssselect('#viewer img.img')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    name = re.search('\\.me/manga/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
