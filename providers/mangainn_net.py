#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'https://www.mangainn.net'
manga_name = ''


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#divIslem + table +  div.divThickBorder .BlackLabel14 a')
    items.reverse()
    return ['https:' + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    idx = volume.rfind('-chapter-')
    if idx > 0:
        return volume[1+idx:]
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
    global manga_name
    if len(manga_name):
        return manga_name
    if url.find('/chapter/') > 0:
        content = get(url)
        url = 'https:' + document_fromstring(content).cssselect('a#gotoMangaInfo')[0].get('href')
    name = re.search('\.net/manga/(\d+_[^/]+)', url)
    if not name:
        return ''
    manga_name = name.groups()[0]
    return manga_name


if __name__ == '__main__':
    print('Don\'t run this, please!')
