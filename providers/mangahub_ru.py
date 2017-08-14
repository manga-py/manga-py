#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
import html

domainUri = 'http://mangahub.ru'
uriRegex = 'https?://(?:www\.)?mangahub\.ru/([^/]+)/?'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None):
    parser = document_fromstring(content)
    parser = parser.cssselect('.b-catalog-list__name a[href^="/"]')
    list = [domainUri + i.get('href') for i in parser]
    list.reverse()
    return list


def get_archive_name(volume, index: int = None):
    parser = re.search('/[^/]+/read/([^/]+)/([^/]+)/([^/]+)/', volume)
    if parser is None:
        return ''
    groups = parser.groups()
    return '{}_{}/{:0>2}'.format(groups[0], groups[1], groups[2])


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    parser = parser.cssselect('.b-main-container .b-reader__full')
    if parser is None:
        return []
    result = parser[0].get('data-js-scans')
    result = json.loads(html.unescape(result.replace('\/', '/')))
    list = [domainUri + i['src'] for i in result]
    return list


def get_manga_name(url, get=None):
    parser = re.search(uriRegex, url)
    if parser is None:
        return ''
    return parser.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
