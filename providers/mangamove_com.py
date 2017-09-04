#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://www.mangamove.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    if not name:
        return ''
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.container .col-md-10 a.btn')
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('/manga/[^/]+/([^/]+)', volume)
    if not result:
        return 'vol_{:0>3}'.format(index)
    return result.groups()[0]


def __get_img(parser):
    return [i.get('src') for i in parser.cssselect('img.manga_image_frame')]


def get_images(main_content=None, volume=None, get=None, post=None):
    parser = document_fromstring(get(volume))
    base_url = volume[0:volume.rfind('/') + 1]
    images = __get_img(parser)
    i = 1 + len(images)

    if len(images) < 2:
        return images

    n = 99
    while n > 0:
        if n == 1: print('Error!!!', '{}/{}'.format(base_url, i))
        n -= 1
        parser = document_fromstring(get('{}/{}'.format(base_url, i)))

        _ = __get_img(parser)
        i += len(_)
        images += _

        # last page test
        page = parser.cssselect('p > a.btn.btn-info + a.btn')[0].get('href')
        if page[page.rfind('/') + 1:] == '1':  # if found next volume
            break

    return images


def get_manga_name(url, get=None):
    name = re.search('\.com/manga/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
