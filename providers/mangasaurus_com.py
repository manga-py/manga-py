#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://mangasaurus.com'
manga_name = ''


def get_main_content(url, get=None, post=None):
    global manga_name
    parser = re.search('\\.com/manga/(\d+)/([^/]+)', url)
    _ = parser.groups()
    manga_name = _[1]
    return get('{}/manga/{}/{}'.format(domainUri, _[0], _[1]))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.table--chapters td > a')
    parser.reverse()
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    path = 'http://img.mangasaurus.com/original/{}/{}-{}.jpg'  # hash, manga_name, image_id
    parser = re.search('ImageReader.setImages.+?(\{.+\})', get(volume))
    if not parser:
        return []
    images = []
    o = json.loads(parser.groups()[0])
    for i in o:
        n = i
        if isinstance(n, str):
            n = o[n]
        _ = n['original']['file']
        src = path.format(_[0:_.find('.')], manga_name, n['id'])
        images.append(src)
    return images


def get_manga_name(url, get=None):
    name = re.search('\\.com/manga/(\d+)/([^/]+)', url)
    if not name:
        raise UrlParseError()
    _ = name.groups()
    return '{}_{}'.format(_[0], _[1])
