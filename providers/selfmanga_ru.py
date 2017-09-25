#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://selfmanga.ru'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}'.format(domainUri, name)
    return get(url + '?mature=1')


def get_volumes(content: str, url=None, get=None, post=None):
    parser = document_fromstring(content)
    parser = parser.cssselect('#mangaBox > div.leftContent div.chapters-link tr > td > a')
    if not parser:
        return []
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('/.+?/(.+?/.+)/?', volume)
    if not result:
        return 'vol_{}'.format(index)
    return result.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    result = re.search('rm_h\.init.+?(\[\[.+\]\])', content, re.M)
    if not result:
        return []
    return [i[1] + i[0] + i[2] for i in json.loads(result.groups()[0].replace("'", '"'))]


def get_manga_name(url, get=None):
    result = re.search('\.ru/([^/]+)/?', url)
    if not result:
        raise UrlParseError()
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
