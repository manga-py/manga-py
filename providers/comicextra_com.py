#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.comicextra.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/comic/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#list a[href*="/chapter"]')
    return ['{}/full'.format(i.get('href')) for i in items]


def get_archive_name(volume, index: int = None):
    i = re.search('chapter-(\d+)', volume)
    return 'vol_{}'.format(i.groups()[0]) if i else 'vol__{}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    items = document_fromstring(get(volume)).cssselect('.chapter-container img.chapter_img')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    test = re.search('\\.com/comic/([^/+])', url)
    if test:
        return test.groups()[0]
    test = re.search('\\.com/([^/]+)/chapter', url)
    if test:
        return test.groups()[0]
    raise UrlParseError()
