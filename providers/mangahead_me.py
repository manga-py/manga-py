#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://mangahead.me'


def get_main_content(url, get=None, post=None):
    parser = re.search('\\.me/(?:index.php/)?(Manga-\w+-Scan/)([^/]+)', url).groups()
    return get('{}/{}/{}'.format(domainUri, parser[1], parser[1]))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('table table table a[href^="/"]')
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.me/(?:Manga-\w+-Scan/)?[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    tmb_selector = '#main_content .mangahead_thumbnail_cell a[name]'
    content = get(volume)
    parser = document_fromstring(content).cssselect(tmb_selector)
    if len(parser) < 1:
        return []
    pages = document_fromstring(content).cssselect('table + .mangahead_pages_navigator a:not(:last-child)')
    _ = document_fromstring(get(domainUri + parser[0].get('href'))).cssselect('#mangahead_image')[0].get('src')
    img_uri = _[0: 1 + _.rfind('/')]
    images = [img_uri + i.get('name') for i in parser]
    if len(pages):
        for i in pages:
            content = get(domainUri + i.get('href'))
            parser = document_fromstring(content).cssselect(tmb_selector)
            if len(parser):
                images += [img_uri + i.get('name') for i in parser]
    return images


def get_manga_name(url, get=None):
    name = re.search('\\.me/(?:index.php/)?(?:Manga-\w+-Scan/)?([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
