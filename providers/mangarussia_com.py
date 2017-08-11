#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://www.mangarussia.com'
uriRegex = 'https?://(?:www\.)?mangarussia\.com/manga/([^/]+)\.html'


def test_url(url):
    test = re.match(uriRegex, url)
    if test is None:
        return False
    return len(test.groups()) > 0


def get_main_content(url, get=None, post=None):
    return get(url)


def get_volumes(content=None, url=None):
    parser = document_fromstring(content)
    result = parser.cssselect('.chapterlist .col1 > a')
    if result is None:
        return []
    list = [i.get('href') for i in result]
    list.reverse()
    return list


def get_archive_name(volume, index: int = None):
    # fucking names :[
    result = re.search('\+(\d+)\+\-\+(\d+)\+.+/(\d+)', volume)
    if result is None:
        return ''
    _ = result.groups()
    return '{:0>2}_{:0>3}/{}'.format(_[0], _[1], _[2])


def __get_img(parser):
    return parser.cssselect('img#comicpic')[0].get('src')


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = document_fromstring(content)
    result = parser.cssselect('select#page option')
    pages_list = [value.get('value') for index, value in enumerate(result) if index]  # skip first page
    first_image = __get_img(parser)
    images = [first_image]
    for i in pages_list:
        content = get(i)
        parser = document_fromstring(content)
        images.append(__get_img(parser))
    return images


def get_manga_name(url, get=None):
    result = re.search(uriRegex, url)
    if result is not None:
        return result.groups()[0].replace('+', ' ')
    return ''


if __name__ == '__main__':
    print('Don\'t run this, please!')
