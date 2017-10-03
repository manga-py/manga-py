#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://readms.net'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.table-striped td > a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.com/r/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def _get_image(parser):
    items = parser.cssselect('img#manga-page')
    return items[0].get('src') if len(items) else None


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    images = [_get_image(parser)]
    pages = parser.cssselect('.btn-reader-page .dropdown-menu li + li a')

    for i in pages:
        content = get(i.get('href'))
        parser = document_fromstring(content)
        images.append(_get_image(parser))

    return images


def get_manga_name(url, get=None):
    name = re.search('\\.net/manga/([^/]+)', url)
    if not name:
        name = re.search('\\.net/r/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
