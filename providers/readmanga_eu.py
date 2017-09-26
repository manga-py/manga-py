#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.readmanga.eu'


def get_main_content(url, get=None, post=None):
    name = re.search('\\.eu/(manga/\d+/[^/]+)', url)
    if not name:
        return ''
    return get('{}/{}'.format(domainUri, name.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#chapters_b > span > a[href*="/manga/"]')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('/manga/\d+/[^/]+/([^/]+/[^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0].replace('/', '_')


def get_images(main_content=None, volume=None, get=None, post=None):
    images_class = '.mainContent img.ebook_img'
    parser = document_fromstring(get(domainUri + volume))
    pages = parser.cssselect('#jumpto > option')
    images = []
    for n, i in enumerate(pages):
        if n > 1:
            option = document_fromstring(get(domainUri + i.get('value')))
        else:
            option = parser
        content = option.cssselect(images_class)
        for j in content:
            images.append(j.get('src'))
    return images


def get_manga_name(url, get=None):
    name = re.search('\\.eu/manga/\d+/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
