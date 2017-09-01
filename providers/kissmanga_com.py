#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
# import json

domainUri = 'http://kissmanga.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/Manga/{}'.format(domainUri, url))


def get_volumes(content=None, url=None):
    items = document_fromstring(content).cssselect('.listing td a')
    return [domainUri + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('.+/(.+?).Read\-Online', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    """
    :param main_content: mixed (1)
    :param volume: mixed (2)
    :param get: request.get
    :param post: request.post
    :return: dict(str)
    """
    pass


def get_manga_name(url, get=None):
    name = re.search('\.com/Manga/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
