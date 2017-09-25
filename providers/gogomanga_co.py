#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'https://gogomanga.co'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}.html'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.list-chapter ul li a')
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    _ = get_manga_name(volume)
    name = re.search('/([^/]+)?\.html', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    name = name.groups()[0]
    return 'vol_{}'.format(name[1 + len(_):])


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content).cssselect('.list-image li img')
    return [i.get('src') for i in parser]


def get_manga_name(url, get=None):
    name = re.search('\.co/(?:manga/)?([^/]+)(?:/[^/]+)?.html', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
