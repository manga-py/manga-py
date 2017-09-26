#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangareader.net'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    result = document_fromstring(content).cssselect('#listing a')
    result.reverse()
    return [domainUri + i.get('href') for i in result]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.net/.+?/(\d+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0]


def __get_img(parser):
    return parser.cssselect('#img')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('select#pageMenu option')
    pages_list = [value.get('value') for index, value in enumerate(result) if index]  # skip first page
    first_image = __get_img(parser)
    images = [first_image]
    for i in pages_list:
        content = get(domainUri + i)
        parser = document_fromstring(content)
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    result = re.search('\\.net/([^/]+)', url)
    if not result:
        raise UrlParseError()
    return result.groups()[0]
