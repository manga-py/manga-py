#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'https://mangaclub.ru'
uriRegex = 'https?://(?:www\.)?mangaclub\.ru(?:/manga/view)?/(\d+\-[^/]+)/?'


def test_url(url):
    test = re.match(uriRegex, url)
    if test is None:
        return False
    return len(test.groups()) > 0


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}.html'.format(domainUri, name)
    return get(url)


def get_volumes(content: str, url=None):
    parser = document_fromstring(content)
    result = parser.cssselect('.manga-ch-list a.col-sm-10')
    if result is None:
        return []
    list = [i.get('href') for i in result]
    list.reverse()
    return list


def get_archive_name(volume, index: int = None):
    result = re.search('/manga/view/.+/([^.]+).html', volume)
    return result.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('.manga-lines-page a.manga-lines')
    return [i.get('data-i') for i in result]


def get_manga_name(url, get=None):
    test = re.search(uriRegex + '\.html', url)
    if test is not None:
        return test.groups()[0]
    return re.search(uriRegex, url).groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
