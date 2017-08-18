#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re

domainUri = 'http://tenmanga.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url, get)
    return get('{}/book/{}.html'.format(domainUri, name))


def get_volumes(content=None, url=None):
    items = document_fromstring(content).cssselect('.chapter-name.long > a')
    return [i.get('href') + '1-150-1.html' for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    items = document_fromstring(get(volume)).cssselect('.pic_box img.manga_pic')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    _ = '\.com/book/([^/]+)'
    test = re.search(_, url)
    if test:
        return test.groups()[0]
    test = re.search('\.com/chapter/.+', url)
    if test:
        test = document_fromstring(get(url)).cssselect('.read-page nav a[href*="/book/"]')
        if len(test):
            test = re.search(_, test[0].get('href'))
            return test.groups()[0]
    return ''


if __name__ == '__main__':
    print('Don\'t run this, please!')
