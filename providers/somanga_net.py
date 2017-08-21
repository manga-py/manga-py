#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://somanga.net'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('ul.capitulos li > a')
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('\.net/[^/]+/[^/]+/([^/]+)', volume)
    if not name:
        return ''
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    parser = document_fromstring(get(volume)).cssselect('img.img-manga')
    return [i.get('src') for i in parser]


def get_manga_name(url, get=None):
    name = re.search('\.net/[^/]+/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
