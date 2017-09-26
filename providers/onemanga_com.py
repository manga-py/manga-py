#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.onemanga.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.magaslistslistc .chapter-title-rtl a')
    items = [i.get('href') for i in parser]
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    parser = re.search('/manga/[^/]+/([^/]+)', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    # TODO! Site crashed now
    pass


def get_manga_name(url, get=None):
    result = re.search('\\.com/manga/([^/]+)', url)
    if not result:
        raise UrlParseError()
    return result.groups()[0]
