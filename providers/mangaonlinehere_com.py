#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://mangaonlinehere.com'
uriRegex = 'https?://(?:www.)?mangaonlinehere.com/manga\-info/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga-info/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('.list-chapter a')
    if not parser:
        return []
    items = [domainUri + i.get('href') for i in parser]
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = document_fromstring(content).cssselect('#list-img img')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    name = re.search(uriRegex, url)
    return name.groups()[0].strip('-')


if __name__ == '__main__':
    print('Don\'t run this, please!')
