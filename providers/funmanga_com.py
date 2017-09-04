#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://funmanga.com'


def get_main_content(url, get=None, post=None):
    return get('{}/{}'.format(domainUri, get_manga_name(url, get)))


def get_volumes(content=None, url=None):
    items = document_fromstring(content).cssselect('.chapter-list li > a')
    return [i.get('href') + '/all-pages' for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\.com/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    parser = document_fromstring(get(volume))
    return [i.get('src') for i in parser.cssselect('.content-inner > img.img-responsive')]


def get_manga_name(url, get=None):
    name = re.search('\.com/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
