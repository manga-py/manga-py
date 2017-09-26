#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

domainUri = 'https://com-x.life'


def get_main_content(url, get=None, post=None):
    manga_id = re.search('\\.life/readcomix/\d+', url)
    if manga_id:
        content = document_fromstring(get(url)).cssselect('#dle-speedbar > a')
        return get(content[0].get('href'))
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#dle-content ul.comix-list li a:not([style])')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    prefix = domainUri + '/comix/'
    content = get(domainUri + volume)
    images = re.search('comix_images.*?(\[.+?\])', content)
    if not images:
        return []
    images = json.loads(images.groups()[0].replace("'", '"'))
    return [prefix + i for i in images]


def get_manga_name(url, get=None):
    test = re.search('\\.life/readcomix/.+\\.html', url)
    if test:
        parser = document_fromstring(get(url)).cssselect('#dle-speedbar > a')
        url = '.life' + parser[0].get('href')
    name = re.search('\\.life/\d+\-(.+)\\.html', url)
    if not name:
        raise UrlParseError()
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
