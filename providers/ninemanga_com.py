#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from urllib.parse import urlparse
from helpers.exceptions import UrlParseError


def __get_domain(uri):
    url = urlparse(uri)
    return '{}://{}'.format(url.scheme, url.netloc)


def get_main_content(url, get=None, post=None):
    return get('{}/manga/{}.html'.format(__get_domain(url), get_manga_name(url, get)))


def get_volumes(content: str, url=None, get=None, post=None):
    parser = document_fromstring(content)
    result = parser.cssselect('.chapterbox li a.chapter_list_a')
    if not result:
        return []
    items = []
    url = __get_domain(url)
    for i in result:
        u = re.search('(/chapter/.*/\d+)\\.html', i.get('href'))
        if u is not None:
            img = u.groups()
            # lifehack
            items.append('{}{}-150-1.html'.format(url, img[0]))
    return items


def get_archive_name(volume, index: int = None):
    return 'vol_{}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    # fucking guards :[
    content = get(volume)
    pic_url = re.search('img_url\s?=\s?"([^"]+)', content).groups()[0]

    if pic_url.find('taadd.com') > 0:
        pic_url = 'https://pic3.taadd.com'

    parser = document_fromstring(content)
    result = parser.cssselect('em a.pic_download')
    if not result:
        return []

    images = []

    for i in result:
        src = i.get('href')
        uri = re.search('://.+?//?(.+)', src).groups()[0]
        images.append('{}/{}'.format(pic_url, uri))

    return images


def get_manga_name(url, get=None):
    result = re.search('\\.com/manga/(.+)\\.html', url)
    if not result:
        raise UrlParseError
    return result.groups()[0]
