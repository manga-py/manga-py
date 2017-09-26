#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'https://bato.to'
manga_name = None


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    _ = '{}/comic/_/comics/{}'.format(domainUri, name)
    return get(_)


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.chapters_list a[href*="/reader#"]')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = _get_content(volume, get)
    parser = document_fromstring(content)
    pages = parser.cssselect('#page_select')[0].cssselect('option + option')
    images = [parser.cssselect('img#comic_page')[0].get('src')]
    for i in pages:
        n = 1
        i = i.get('value')
        if i.find('_'):
            n = i.split('_')[1]
        content = _get_content(volume, get, n)
        img = document_fromstring(content).cssselect('img#comic_page')[0].get('src')
        images.append(img)
    return images


def get_manga_name(url, get=None):
    global manga_name
    if manga_name:
        return manga_name
    test = re.search('\\.to/reader', url)
    if test:
        content = _get_content(url, get)
        _url = document_fromstring(content).cssselect('li > a[href*="/comics"]')
        if len(_url):
            url = _url[0].get('href')
    name = re.search('/comics/([^/]+)', url)
    if not name:
        raise UrlParseError()
    manga_name = name.groups()[0]
    return manga_name


def _get_content(url, get, p=1):
    if url.find('#') < 5:
        raise UrlParseError()
    _hash = url.split('#')[1]
    if _hash.find('_') > 0:
        _hash = _hash.split('_')[0]
    api_uri = 'https://bato.to/areader?id={}&p={}'.format(_hash, p)
    return get(api_uri, headers={'Referer': 'https://bato.to/reader'})
