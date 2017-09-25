#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangahome.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('.detail-chlist a')
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('/manga/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0]


def _content2image_url(content):
    parser = document_fromstring(content)
    result = parser.cssselect('img#image')
    return result[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    pages = document_fromstring(content)
    items = pages.cssselect('.mangaread-top .mangaread-pagenav select option')
    pages = [i.get('value') for n, i in enumerate(items) if n > 0]

    images = [_content2image_url(content)]

    for i in pages:
        content = get(i)
        images.append(_content2image_url(content))

    return images


def get_manga_name(url, get=None):
    name = re.search('\.com/manga/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
