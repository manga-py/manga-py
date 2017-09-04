#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.cloudflare_scrape import cfscrape

domainUri = 'http://kissmanga.com'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/Manga/{}'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.listing td a')
    return [domainUri + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    name = re.search('/Manga/[^/]+/([^/\?]+)', volume)
    if not name:
        return 'vol_{:0>3}'.format(index)
    return name.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    # see storage/1.js
    pass


def get_manga_name(url, get=None):
    name = re.search('\.com/Manga/([^/]+)', url)
    global cookies

    if not cookies:
        # anti-"cloudflare anti-bot protection"
        scraper = cfscrape.get_tokens(url)
        if scraper is not None:
            cookies = []
            for i in scraper[0]:
                cookies.append({
                    'value': scraper[0][i],
                    'domain': '.kissmanga.com',
                    'path': '/',
                    'name': i,
                })
            cookies.append(scraper[1])
    if not name:
        return ''
    return name.groups()[0]


cookies = None


if __name__ == '__main__':
    print('Don\'t run this, please!')
