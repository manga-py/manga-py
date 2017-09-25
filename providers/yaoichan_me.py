#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'http://yaoichan.me'
imagesRegex = '"fullimg":\s?\[(.*)?\]'


def get_main_content(url, get=None, post=None):
    if re.search('me/online/\d+\-', url):
        content = get(url)
        parser = re.search('"content_id":\s?"(.+)",', content)
        if parser:
            url = domainUri + parser.groups()[0]
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('td .manga > a')
    if not parser:
        return []
    return [domainUri + i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    parser = re.search('_(v\d+_ch\d+)', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = re.search(imagesRegex, content)
    if not parser:
        return []
    parser = parser.groups()[0].rstrip(',')
    items = json.loads('[' + parser + ']')
    return items


def get_manga_name(url, get=None):
    parser = re.search('\.me/.+/\d+\-(.*)\.html', url)
    if not parser:
        raise UrlParseError()
    return parser.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
