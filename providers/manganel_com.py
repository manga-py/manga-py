#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
from lxml.html import document_fromstring

domainUri = 'http://manganel.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('.chapter-list span a')
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('chapter/[^/]+/([^/]+)', volume)
    if not result:
        return 'vol_{}'.format(index)
    return result.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    result = document_fromstring(content).cssselect('#vungdoc img')
    return [i.get('src') for i in result]


def get_manga_name(url, get=None):
    result = re.search('/(?:manga|chapter)/([^/]+)/?', url)
    if not result:
        return ''
    name = result.groups()
    return name[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
