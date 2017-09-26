#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'https://www.mangabox.me'
content = ''


def get_main_content(url, get=None, post=None):
    if len(content) > 0:
        return content
    name = get_manga_name(url, get)
    return get('{}/reader/{}/'.format(domainUri, name.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    return ['0']


def get_archive_name(volume, index: int = None):
    return volume


def get_images(main_content=None, volume=None, get=None, post=None):
    return [i.get('src') for i in document_fromstring(main_content).cssselect('ul.slides img.jsNext')]


def get_manga_name(url, get=None):
    global content
    if not len(content):
        content = get_main_content(url, get)
    name = re.search('\s+?\<h2\>[^.]+?\n?([\w\s-]+?)\n', content)
    if not name:
        name = re.search('/reader/(\d+)', url)
        if not name:
            raise UrlParseError()
    return name.groups()[0]
