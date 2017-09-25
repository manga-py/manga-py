#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangabb.co'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    content = get('{}/manga/{}'.format(domainUri, name))
    parser = document_fromstring(content)
    result = parser.cssselect('#chapters a')

    return result[0].get('href') if len(result) else False


def get_volumes(content=None, url=None, get=None, post=None):
    if not content:
        return []

    downloaded_content = get(content)

    selector = '#manga_nav_top select.chapter_select > option'
    result = document_fromstring(downloaded_content).cssselect(selector)

    items = [i.get('value') for i in result]

    return items


def get_archive_name(volume, index: int = None):
    idx = volume.rfind('/chapter-')
    if idx > 0:
        return volume[1+idx:]
    return 'vol_{:0>3}'.format(index)


def __get_img(parser):
    return parser.cssselect('#manga_viewer > a > img')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('#asset_2 select.page_select option')
    pages_list = [i.get('value') for n, i in enumerate(result) if n > 0]
    _first_image = __get_img(parser)
    images = [_first_image]

    img = re.search('(.+/)\d(\.\w+)', _first_image)
    if img:  # livehack
        img = img.groups()
        n = 1
        for i in pages_list:
            n += 1
            images.append('{}{}{}'.format(img[0], n, img[1]))
    else:
        for page in pages_list:
            content = get(page)
            parser = document_fromstring(content)
            images.append(__get_img(parser))

    return images


def get_manga_name(url, get=None):
    result = re.search('\.co/(?:manga/)?([^/]+)', url)
    if not result:
        raise UrlParseError()
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
