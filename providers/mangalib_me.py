#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'https://mangalib.me'


def get_main_content(url, get=None, post=None):
    return get('{}/{}'.format(domainUri, get_manga_name(url)))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.vol_lst li h5 a')
    return [i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('\.me/[^/]+/([^/]+/[^/]+)', volume)
    if not name:
        return 'vol_{}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    _id = re.search('var\s+currentId.+?=.+?(\d+)', content)
    if not _id:
        return []
    try:
        uri = domainUri + '/pages/' + _id.groups()[0]
        items = json.loads(get(uri))
    except Exception:
        return []
    href = re.search('[\'"](http[^\'"]+)[\'"].+\.page_image', content)
    if not href:
        _ = re.search('(\d+)/.?(\d+)', volume).groups()
        href = 'https://img1.mangalib.me/manga/one-piece/chapters/' + _[0] + '-' + _[1]
    else:
        href = href.groups()[0].strip('/') + '/'
    return [href + i['page_image'] for i in items['pages']]


def get_manga_name(url, get=None):
    name = re.search('\.me/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
