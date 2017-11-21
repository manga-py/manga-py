#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://readcomicbooksonline.net'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#chapterlist .chapter > a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    i = re.search('_chapter_(\d+)', volume)
    return 'vol_{}'.format(i.groups()[0]) if i else 'vol__{}'.format(index)


def _get_image(p):
    src = p.cssselect('a > img.picture')
    if not src:
        return None
    return '{}/reader/{}'.format(domainUri, src[0].get('src'))


def _get_doc_f_str(uri, get):
    return document_fromstring(get(uri))


def get_images(main_content=None, volume=None, get=None, post=None):
    content = _get_doc_f_str(volume, get)
    pages = [i.get('value') for i in content.cssselect('.pager select[name="page"]')[0].cssselect('option + option')]
    img = _get_image(content)
    images = []
    if img:
        images.append(img)
    for i in pages:
        _content = _get_doc_f_str('{}/{}'.format(volume, i), get)
        img = _get_image(_content)
        if img:
            images.append(img)
    return images


def get_manga_name(url, get=None):
    test = re.search('\\.net/reader/([^/]+)', url)
    if test:
        return test.groups()[0]
    test = re.search('\\.net/([^/]+)$', url)
    if test:
        return test.groups()[0]
    raise UrlParseError()
