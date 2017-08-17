#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://mintmanga.com'
uriRegex = '\.com/([^/]+)/?'
imagesRegex = 'rm_h\.init.+?(\[\[.+\]\])'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}'.format(domainUri, name)
    return get(url + '?mtr=1')


def get_volumes(content: str, url=None):
    parser = document_fromstring(content)
    result = parser.cssselect('#mangaBox > div.leftContent div.chapters-link tr > td > a')
    if result is None:
        return []
    list = [i.get('href') for i in result]
    list.reverse()
    return list


def get_archive_name(volume, index: int = None):
    result = re.search('/.+?/(.+?/.+)/?', volume)
    name = result.groups()
    name = name[0]
    if name.find('?') > 0:
        name = name[0:name.find('?')]
    return name  # .replace('/', '_')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    result = re.search(imagesRegex, content, re.M)
    if result is None:
        return []
    return [i[1] + i[0] + i[2] for i in json.loads(result.groups()[0].replace("'", '"'))]


def get_manga_name(url, get=None):
    result = re.match(uriRegex, url)
    if result is None:
        return ''
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
