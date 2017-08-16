#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://desu.me'
uriRegex = 'https?://(?:www\.)?desu\.me/manga/([^/]+)/?'
imagesDirRegex = 'dir:\s?"(.*)"'
imagesRegex = 'images:\s?(\[\[.+\]\])'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/manga/{}'.format(domainUri, name)
    return get(url)


def get_volumes(content: str, url=None):
    parser = document_fromstring(content).cssselect('#animeView ul h4 > a.tips')
    if parser is None:
        return []
    parser.reverse()
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('/manga/.+?/(.+?/.+)/', volume)
    name = result.groups()
    return name[0]  # .replace('/', '_')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    result = re.search(imagesRegex, content, re.M)
    root_url = re.search(imagesDirRegex, content, re.M)
    if result is None:
        return []
    root_url = root_url.groups()[0].replace('\\/', '/')
    result = [root_url + i[0] for i in json.loads(result.groups()[0])]
    return result


def get_manga_name(url, get=None):
    result = re.match(uriRegex, url)
    if result is None:
        return ''
    result = result.groups()
    if not len(result):
        return ''
    return result[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
