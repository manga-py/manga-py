#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://www.mangahere.co'
uriRegex = '/manga/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    print('{}/{}'.format(domainUri, name))
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('.detail_list .left a')
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('/manga/.+?/([^/]+)', volume)
    if not name:
        return index
    return name.groups()[0]


def __get_img(parser):
    return parser.cssselect('img#image')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('.go_page select.wid60 option')
    pages_list = [value.get('value') for index, value in enumerate(result) if index]  # skip first page
    first_image = __get_img(parser)
    images = [first_image]
    for i in pages_list:
        content = get(i)
        parser = document_fromstring(content)
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    result = re.search(uriRegex, url)
    if not result:
        return ''
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
