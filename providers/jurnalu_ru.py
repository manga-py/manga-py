#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.exceptions import UrlParseError

domainUri = 'http://jurnalu.ru'


def get_main_content(url, get=None, post=None):
    name = re.search('(online\-reading/[^/]+/[^/]+)', url)
    content = document_fromstring(get('{}/{}'.format(domainUri, name.groups()[0])))
    content = content.cssselect('.MagList .MagListLine > a')[0].get('href')
    return get(domainUri + content)


def get_volumes(content=None, url=None, get=None, post=None):
    name = re.search('(online\-reading/[^/]+/[^/]+)', url)
    if not name:
        return []
    items = document_fromstring(content).cssselect('select.magSelection option')
    name = name.groups()[0]
    return ['{}/{}/{}'.format(domainUri, name, i.get('value')) for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def __get_img(parser):
    image = parser.cssselect('.ForRead a[rel="shadowbox"]')
    return image[0].get('href')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    page = document_fromstring(content)
    parser = document_fromstring(content).cssselect('.ForRead .navigation')
    pages = parser[0].cssselect('select.M option + option')
    images = [__get_img(page)]
    for i in pages:
        uri = '{}/{}'.format(volume, i.get('value'))
        parser = document_fromstring(get(uri))
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    name = re.search('\\.ru/online\-reading/[^/]+/([^/]+)', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
