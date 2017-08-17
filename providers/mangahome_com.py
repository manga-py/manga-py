#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://www.mangahome.com'
uriRegex = 'https?://(?:www.)?mangahome\.com/manga/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    parser = document_fromstring(content).cssselect('.detail-chlist a')
    parser.reverse()
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    name = re.search('/manga/[^/]+/([^/]+)', volume)
    if not name:
        return ''
    return name.groups()[0]


def _content2image_url(content):
    parser = document_fromstring(content)
    result = parser.cssselect('img#image')
    return result[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    _url = (domainUri + volume) if volume.find(domainUri) < 0 else volume
    content = get(_url)
    pages = document_fromstring(content)
    pages = [i.get('value') for n, i in enumerate(pages.cssselect('.mangaread-top .mangaread-pagenav select option')) if n > 0]

    images = [_content2image_url(content)]

    for i in pages:
        content = get(i)
        images.append(_content2image_url(content))

    return images


def get_manga_name(url, get=None):
    name = re.search(uriRegex, url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
