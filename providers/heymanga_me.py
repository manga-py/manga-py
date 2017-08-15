#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'https://www.heymanga.me'
uriRegex = 'https?://(?:www.)?heymanga\.me/manga/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    result = document_fromstring(content).cssselect('#chapters .ti-heart a')
    if not result:
        return []
    list = [domainUri + i.get('href') for i in result]
    list.reverse()
    return list


def get_archive_name(volume, index: int = None):
    result = re.search('/manga/[^/]+/([^/]+)', volume)
    if not result:
        return 'vol_{}'.format(index)
    return result.groups()[0]


def __get_img(parser):
    return ['https:' + i.get('src') for i in parser.cssselect('.img-fill')]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('#fuzetsu_list option[value]')
    pages_list = [i.get('value') for i in result]
    images = __get_img(parser)
    index = len(images)
    root_volume_uri = volume[0: volume.rfind('/')]
    _len = len(pages_list) - 1
    while index < _len:
        url = '{}/{}'.format(root_volume_uri, pages_list[index])
        content = get(url)
        parser = document_fromstring(content)
        _ = __get_img(parser)
        index = len(_) + index
        images += _
    return images


def get_manga_name(url, get=None):
    result = re.search(uriRegex, url)
    if not result:
        return ''
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
