#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://www.rawdevart.com'


def get_main_content(url, get=None, post=None):
    content = get(url)
    chapters = document_fromstring(content).cssselect('select.select-chapter script')[0].get('src')
    chapters = re.search('usagislct\\(({.+})\\)', get(domainUri + chapters)).group(1)
    result = json.loads(chapters)
    return result.get('feed', {}).get('entry', [])


def _get_link(items, url_len):
    for i in items:
        if str(i['rel']) == 'alternate' and len(i['href']) > url_len:
            return i['href']
    return None


def get_volumes(content=None, url=None, get=None, post=None):
    url_len = len(url)
    items = []
    for i in content:
        uri = _get_link(i['link'], url_len)
        if uri:
            items.append(uri)
    return items


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = document_fromstring(content).cssselect('.separator img[src]')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    name = get(url)
    name = document_fromstring(name).cssselect('h2.post-title.entry-title')[0].text_content()
    print(name)
    return name
