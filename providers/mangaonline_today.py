#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://www.mangaonline.today'


def get_main_content(url, get=None, post=None):
    return get('{}/{}/'.format(domainUri, get_manga_name(url, get)))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('ul.chp_lst a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\\.today/[^/]+/([^/]+)', volume)
    if not name:
        return 'vol__{}'.format(index)
    return 'vol_{}'.format(name.groups()[0])


def get_images(main_content=None, volume=None, get=None, post=None):
    images = []
    content = document_fromstring(get(volume))
    options = len(content.cssselect('.cbo_wpm_pag')[0].cssselect('option')) / 2 + 0.5
    img = content.cssselect('#sct_content img')
    if img:
        images = [i.get('src') for i in img]

    for n in range(1, int(options)):
        content = document_fromstring(get('{}{}/'.format(volume, n)))
        img = content.cssselect('#sct_content img')
        for i in img:
            images.append(i.get('src'))

    return images


def get_manga_name(url, get=None):
    name = re.search('\\.today/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
