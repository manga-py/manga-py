#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

magicRegexp = '(https?://[^/]+)/(?:read\-manga/)?([^/]+)'
domainUri = ''


def get_main_content(url, get=None, post=None):
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content)
    select = parser.cssselect('.mid .pager select[name="chapter"]')[0]
    items = select.cssselect('option')
    volume_root_uri = re.search('({})'.format(magicRegexp), url).groups()[0]
    return ['{}/{}/'.format(volume_root_uri, i.get('value')) for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search(magicRegexp + '/([^/]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[2]


def __images_helper(page, volume):

    image = page.cssselect('a > img.picture')

    if not len(image):
        return False

    image = image[0].get('src')
    if image[0] == '/':
        return domainUri + image

    base_uri = page.cssselect('base')
    if len(base_uri):
        base_uri = base_uri[0].get('href')
    else:
        base_uri = volume

    return base_uri + image


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    select = parser.cssselect('.mid .pager select[name="page"]')[0]

    images = []
    _img = __images_helper(parser, volume)

    items = select.cssselect('option + option')

    if _img:
        images.append(_img)
    for i in items:
        page = document_fromstring(get('{}{}/'.format(volume, i.get('value'))))

        _img = __images_helper(page, volume)
        if _img:
            images.append(_img)

    return images


def get_manga_name(url, get=None):
    parser = re.search(magicRegexp, url)
    if not parser:
        raise AttributeError()
    global domainUri
    domainUri = parser.groups()[0]
    return parser.groups()[1]
