#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://eatmanga.me'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/Manga-Scan/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('#updates li a[href^="/M"]')
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = get_manga_name(volume)
    idx = volume.strip('/').rfind('/')
    if idx < 0:
        return 'vol_{:0>3}'.format(index)
    return volume[idx + len(name) + 2:-1]


def __get_img(parser):
    img = parser.cssselect('#eatmanga_image_big')
    if not len(img):
        img = parser.cssselect('#eatmanga_image')
    if not len(img):
        return False
    return img[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    images = [__get_img(parser)]
    result = parser.cssselect('#pages')[0].cssselect('option[value*="page-"]')
    pages_list = [domainUri + i.get('value') for i in result]

    for page in pages_list:
        content = get(page)
        img = __get_img(document_fromstring(content))
        if img:
            images.append(img)
        else:
            pass
    return images


def get_manga_name(url, get=None):
    name = re.search('\\.me/(?:upcoming/)?(?:Manga-Scan/)?([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
