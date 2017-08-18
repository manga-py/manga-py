#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://mangaleader.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/read-online-{}.php'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('#header-image select:first-child option')
    return [i.get('value') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('\.com/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return 'vol_{:0>3}'.format(name.groups()[0])


def __get_img(parser):
    return domainUri + parser.cssselect('#image a > img')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    # need skip first two links and last link
    parser = document_fromstring(get(volume))
    images = [__get_img(parser)]
    parser = parser.cssselect('#navigation a:not([title])')
    l = len(parser) - 1
    pages = [i.get('href') for n, i in enumerate(parser) if 1 < n < l]
    for i in pages:
        parser = document_fromstring(get(i))
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    name = re.search('\.com/read(?:-online)?\-([^/]+?)(?:/|\.php)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
