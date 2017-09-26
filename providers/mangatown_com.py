#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://www.mangatown.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.chapter_list a')
    if not parser:
        return []
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    parser = re.search('/manga/[^/]+/([^/]+)', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def _content2image_url(content):
    parser = document_fromstring(content)
    result = parser.cssselect('img#image')
    return result[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    pages = document_fromstring(content)
    pages = [i.get('value') for n, i in enumerate(pages.cssselect('#top_chapter_list + .page_select select option')) if n > 0]

    images = [_content2image_url(content)]

    for i in pages:
        content = get(i)
        images.append(_content2image_url(content))

    return images


def get_manga_name(url, get=None):
    name = re.search('\\.com/manga/([^/]+)/?', url)
    return name.groups()[0]
