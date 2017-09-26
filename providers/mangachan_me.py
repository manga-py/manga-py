#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://mangachan.me'
manga_name = ''


def get_main_content(url, get=None, post=None):
    get_manga_name(url, get)
    return get('{}/manga/{}.html'.format(domainUri, manga_name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('div.manga a')
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    images = re.search('"fullimg":\s*(\[.+\])', content)
    if not images:
        return []
    images = images.groups()[0].replace(',]', ']')
    return json.loads(images)


def get_manga_name(url, get=None):
    global manga_name

    if len(manga_name):
        return manga_name.split('-', 1)[1]

    if re.search('/online/[^/]+', url):
        url = document_fromstring(get(url)).cssselect('.postload a.a-series-title.manga-title')[0].get('href')
    name = re.search('/[^/]+/(\d+)\-([^/]+)\\.html', url)

    if not name:
        raise UrlParseError()
    groups = name.groups()
    manga_name = '{}-{}'.format(groups[0], groups[1])

    return groups[1]
