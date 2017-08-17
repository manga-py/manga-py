#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'https://www.mangainn.net'
uriRegex = 'https?://(?:www.)?mangainn\.net/manga/(\d+_[^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    items = document_fromstring(content).cssselect('#divIslem + table +  div.divThickBorder .BlackLabel14 a')
    return ['https:' + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    idx = volume.find('chapter-')
    if idx > 0:
        return volume[idx:]
    parser = re.search('/chapter/(\d+)', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def __get_img(parser):
    return 'https:' + parser.cssselect('#imgPage')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('#combopages option[value]')
    pages_list = [i.get('value') for n, i in enumerate(result) if n > 0]
    images = [__get_img(parser)]
    for page in pages_list:
        url = '{}/page_{}'.format(volume, page)
        content = get(url)
        parser = document_fromstring(content)
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    if url.find('/chapter/') > 0:
        content = get(url)
        url = 'https:' + document_fromstring(content).cssselect('a#gotoMangaInfo')[0].get('href')
    name = re.search(uriRegex, url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
