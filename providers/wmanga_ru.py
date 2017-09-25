#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://wmanga.ru'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/starter/manga_byid/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('td div div div td > a')
    parser.reverse()
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('\.ru/starter/manga_[^/]+/[^/]+/([^/]+/[^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    parser = document_fromstring(get(volume)).cssselect('td a.gallery')
    return [i.get('href') for i in parser]


def get_manga_name(url, get=None):
    name = re.search('\.ru/starter/manga_[^/]+/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
