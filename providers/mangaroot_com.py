#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError
from time import sleep

domainUri = 'http://mangaroot.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.chapters .chapter-title-rtl > a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.com/manga/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    print('Sleep ~4 seconds')
    sleep(4)
    content = get(volume)
    items = document_fromstring(content).cssselect('.viewer-cnt #all img[data-src]')
    return [i.get('data-src') for i in items]


def get_manga_name(url, get=None):
    name = re.search('\\.com/manga/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
