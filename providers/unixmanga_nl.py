#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://unixmanga.nl'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    # print(name, '\n', '{}/onlinereading/{}.html'.format(domainUri, name))
    return get('{}/onlinereading/{}.html'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('#mycontent table td a[href*="html"]')
    items = []
    for i in parser:
        url = i.get('href')  # http://unixmanga.nl/onlinereading/13_Club/13_Club_c005.html
        if re.search('/onlinereading/[^/]+/[^/]+\.html', url):
            items.append(url)
    return items


def get_archive_name(volume, index: int = None):
    n = volume.rfind('_')
    if n < 0:
        return 'c{:0>3}'.format(index)
    return volume[1 + n: -5]


def get_images(main_content=None, volume=None, get=None, post=None):
    # http://nas.unixmanga.nl/onlinereading/Kaitou Joker/Kaitou Joker c054/001.jpg
    # http://nas.unixmanga.nl/onlinereading/?image=Kaitou%20Joker/Kaitou%20Joker%20c054/001.jpg&server=nas.html
    content = get(volume)
    parser = document_fromstring(content).cssselect('#news a[href*="server="]')
    images = []
    for i in parser:
        img = re.search('(.+)\?image=(.+).server=.+', i.get('href')).groups()
        images.append(img[0]+img[1])
    return images


def get_manga_name(url, get=None):
    parser = re.search('\.nl/onlinereading/([^/.]+)(?:/[^/])?\.html', url)
    if not parser:
        raise UrlParseError()
    return parser.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
