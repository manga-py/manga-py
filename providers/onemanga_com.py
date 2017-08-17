#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://www.onemanga.com'
uriRegex = 'https?://(?:www.)?onemanga\.com/manga/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None):
    return [i.get('href') for i in document_fromstring(content).cssselect('.magaslistslistc .chapter-title-rtl a')]


def get_archive_name(volume, index: int = None):
    parser = re.search('/manga/[^/]+/([^/]+)', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    # TODO! Now site crashed
    pass


def get_manga_name(url, get=None):
    result = re.match(uriRegex, url)
    if result is None:
        return ''
    return result.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
