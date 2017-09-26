#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

uri_hex = ''
manga_name = ''

domainUri = 'http://inmanga.com'


def get_main_content(url, get=None, post=None):
    if not uri_hex:
        get_manga_name(url)
    uri = '{}/chapter/getall?mangaIdentification={}'.format(domainUri, uri_hex)
    return json.loads(json.loads(get(uri))['data'])


def get_volumes(content=None, url=None, get=None, post=None):
    items = content['result']
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    return str(volume['Number'])


def get_images(main_content=None, volume=None, get=None, post=None):
    uri = '{}/ver/manga/{}/{}/{}'.format(domainUri, manga_name, volume['FriendlyChapterNumber'], volume['Identification'])
    content = get(uri)
    images = document_fromstring(content).cssselect('.PagesContainer img.ImageContainer')
    return ['{}/page/getPageImage/?identification={}'.format(domainUri, i.get('id')) for i in images]


def get_manga_name(url, get=None):
    global uri_hex
    global manga_name
    test = re.search('\\.com/ver/manga/[^/]+/\d+/[^/]+', url)
    if test:
        content = document_fromstring(get(url)).cssselect('.chapterControlsContainer label.blue a.blue')
        url = domainUri + content[0].get('href')
    test = re.search('\\.com/ver/manga/([^/]+)/([^/]+)', url)
    if not test:
        raise UrlParseError()
    groups = test.groups()
    manga_name = groups[0]
    uri_hex = groups[1]
    return groups[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
