#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'https://taadd.com'

def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/book/{}.html'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    return document_fromstring(content).cssselect('.chapter_list td[align="left"] a')
    # return [domainUri + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = volume.text_content().replace('/\:*?"<>|', '_').strip('_')
    return 'vol_{}_{}'.format(index, name)


def __get_image(p):
    return p.cssselect('#comicpic')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    uri = domainUri + volume.get('href')
    content = document_fromstring(get(uri))
    pages = content.cssselect('#page')[0].cssselect('option + option')
    images = [__get_image(content)]

    for i in pages:
        c = document_fromstring(get(i.get('value')))
        images.append(__get_image(c))

    return images


def get_manga_name(url, get=None):
    name = re.search('/book/([^/]+)\\.html', url)
    if not name:
        name = document_fromstring(get(url)).cssselect('h1.chapter_bar .postion .normal a')
        if name:
            return get_manga_name(name[1].get('href'), get)
    if not name:
        raise UrlParseError()
    return name.groups()[0]
