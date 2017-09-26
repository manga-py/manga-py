#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

# site renamed to mangashin.com

# domainUri = 'http://mangatan.net'
domainUri = 'http://mangashin.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.chapter-list .row a')
    if not parser:
        return []
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('/chapter/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content).cssselect('#vungdoc img')
    return [i.get('src') for i in parser]


def get_manga_name(url, get=None):
    name = re.search('\\.(?:net|com)/(?:manga|chapter)/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
