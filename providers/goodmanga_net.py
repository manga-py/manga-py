#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://goodmanga.net'


def get_main_content(url, get=None, post=None):
    if url.find('/chapter/') > 0:
        content = document_fromstring(get(url)).cssselect('#manga_head h3 > a')
        url = content[0].get('href')
    _id = re.search('\.net/(\d+/[^/]+)', url)
    if not _id:
        return ''
    return get('{}/{}'.format(domainUri, _id.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    def get_pages(_parser):
        _pages = _parser.cssselect('#chapters li > a')
        return [i.get('href') for i in _pages]
    if not content:
        return []
    parser = document_fromstring(content)
    pages = get_pages(parser)
    pagination = parser.cssselect('.pagination li > button[href]')  # WTF ?!?!?
    for i in pagination:
        cnt = document_fromstring(get(i.get('href')))
        for n in get_pages(cnt):
            pages.append(n)
    return pages


def get_archive_name(volume, index: int = None):
    test = re.search('/chapter/(\d+)', volume)
    if not test:
        return 'vol_{:0>3}'.format(index)
    return test.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    def get_image(p):
        img = p.cssselect('#manga_viewer > a > img')
        return img[0].get('src')
    parser = document_fromstring(get(volume))
    images = [get_image(parser)]
    for i in parser.cssselect('#asset_2 select.page_select option + option'):
        parser = document_fromstring(get(i.get('value')))
        images.append(get_image(parser))
    return images


def get_manga_name(url, get=None):
    name = re.search('/([^/]+)/chapter/', url)
    if name:
        return name.groups()[0]
    name = re.search('\.net/\d+/([^/]+)', url)
    if name:
        return name.groups()[0]
    raise UrlParseError()


if __name__ == '__main__':
    print('Don\'t run this, please!')
