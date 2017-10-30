#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError
# import json

content = None
domainUri = 'http://mangalife.us'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.chapter-list a.list-group-item')
    return items


def get_archive_name(volume, index: int = None):
    chapter = volume.get('Chapter')
    if chapter is None:
        return 'vol_{:0>3}'.format(index)
    return 'Chapter_{}'.format(chapter)


def _get_images_helper(parser):
    return parser.cssselect('.image-container .CurImage')[0].get('src')


def _uri_helper(url, num):
    u = re.search('(.+-page-)\d+(\\.html)', url)
    u = u.groups()
    return '{}{}{}'.format(u[0], num, u[1])


def get_images(main_content=None, volume=None, get=None, post=None):
    url = '{}{}'.format(domainUri, volume.get('href'))
    content = get(url)
    parser = document_fromstring(content)
    pages = parser.cssselect('select.PageSelect')[0].cssselect('option + option')
    images = [_get_images_helper(parser)]
    for page in pages:
        uri = _uri_helper(url, page.get('value'))
        parser = document_fromstring(get(uri))
        images.append(_get_images_helper(parser))
    return images


def _manga_name_helper(url, get):
    global content
    if not content:
        content = document_fromstring(get(url)).cssselect('a.list-link')
    uri = ''
    if content:
        uri = content[0].get('href')
    return uri


def get_manga_name(url, get=None):
    test = re.search('\\.us/read-online/.+', url)
    uri = url
    if test:
        uri = _manga_name_helper(url, get)
    name = re.search('(?:\\.us)?/manga/([^/]+)', uri)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
