#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
# import json
from helpers.exceptions import UrlParseError

domainUri = 'http://comicsandmanga.ru'


def get_main_content(url, get=None, post=None):
    name = re.search('/online-reading/([^/]+/[^/]+)', url)
    if not name:
        raise UrlParseError()
    return get('{}/online-reading/{}'.format(domainUri, name.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.MagList > .MagListLine > a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('/online-reading/[^/]+/([^/]+)/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    name = name.groups()
    name, fullname = name[0], name[1]
    return fullname[len(name):]


def _images_helper(parser):
    image = parser.cssselect('.ForRead a > img')
    if len(image):
        return image[0].get('src')
    return None


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(domainUri + volume)
    parser = document_fromstring(content)
    pages = parser.cssselect('.ForRead .navigation select')[0].cssselect('option + option')
    images = []
    img = _images_helper(parser)
    if img:
        images.append(img)
    for i in pages:
        uri = '{}/{}/{}'.format(domainUri, volume.rstrip('/'), i.get('value'))
        parser = document_fromstring(get(uri))
        img = _images_helper(parser)
        if img:
            images.append(img)
    return images


def get_manga_name(url, get=None):
    name = re.search('/online-reading/[^/]+/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
