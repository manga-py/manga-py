#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'https://mangalib.me'


def get_main_content(url, get=None, post=None):
    return get('{}/{}'.format(domainUri, get_manga_name(url)))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.vol_lst li h5 a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.me/[^/]+/([^/]+/[^/]+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = re.search('var\s+pages.?=.?(\[{.+?\}])', content)
    items = json.loads(items.groups()[0])
    href = re.search('[\'"](http[^\'"]+)[\'"].+\\.page_image', content)
    if not href:
        _ = re.search('([^/]+)/[^/]+/(\d+)/.?(\d+)', volume).groups()
        href = 'https://img1.mangalib.me/manga/{}/chapters/{}-{}/'.format(_[0],_[1],_[2],)
    else:
        href = href.groups()[0].strip('/') + '/'
    return [href + i['page_image'] for i in items]


def get_manga_name(url, get=None):
    name = re.search('\\.me/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
