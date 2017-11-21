#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import cfscrape
from helpers.exceptions import UrlParseError

domainUri = 'http://readcomiconline.to'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/Comic/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('table.listing td > a')
    return ['{}/{}&readType=1'.format(domainUri, i.get('href')) for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    items = re.findall('lstImages.push\("([^"]+)"\)', content)
    return items


def get_manga_name(url, get=None):

    test = re.search('\\.to/Comic/([^/]+)', url)
    if not test:
        raise UrlParseError()

    global cookies
    if not cookies:
        scraper = cfscrape.get_tokens(url)
        if scraper is not None:
            cookies = []
            for i in scraper[0]:
                cookies.append({
                    'value': scraper[0][i],
                    'domain': '.readcomiconline.to',
                    'path': '/',
                    'name': i,
                })
            cookies.append(scraper[1])

    return test.groups()[0]


cookies = None
