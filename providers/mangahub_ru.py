#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
import html

domainUri = 'http://mangahub.ru'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content)
    parser = parser.cssselect('.b-catalog-list__name a[href^="/"]')
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    parser = re.search('/[^/]+/read/([^/]+)/([^/]+)/([^/]+)/', volume)
    if not parser:
        return 'vol_{}'.format(index)
    groups = parser.groups()
    return '{}_{}/{:0>2}'.format(groups[0], groups[1], groups[2])


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    parser = parser.cssselect('.b-main-container .b-reader__full')
    if not parser:
        return []
    result = parser[0].get('data-js-scans')
    result = json.loads(html.unescape(result.replace('\/', '/')))
    items = [domainUri + i['src'] for i in result]
    return items


def get_manga_name(url, get=None):
    parser = re.search('\.ru/([^/]+)/?', url)
    if not parser:
        return ''
    return parser.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
