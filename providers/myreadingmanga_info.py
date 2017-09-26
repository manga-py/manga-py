#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import cfscrape
from helpers.exceptions import UrlParseError
# import json

domainUri = 'https://myreadingmanga.info'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    return get('{}/{}/'.format(domainUri, name))


def get_volumes(content=None, url=None, get=None, post=None):
    v = [url]  # current chapter
    parser = document_fromstring(content).cssselect('.entry-content p > a')
    v += [i.get('href') for i in parser]
    v.reverse()
    return v


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>2}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    parser = document_fromstring(get(volume)).cssselect('.entry-content div img')
    return [i.get('src') for i in parser]


def get_manga_name(url, get=None):
    # anti-"cloudflare anti-bot protection"
    name = re.search('\\.info/([^/]+)', url)
    if not name:
        raise UrlParseError()

    global cookies
    if not cookies:
        scraper = cfscrape.get_tokens(url)
        if scraper is not None:
            cookies = []
            for i in scraper[0]:
                cookies.append({
                    'value': scraper[0][i],
                    'domain': '.myreadingmanga.info',
                    'path': '/',
                    'name': i,
                })
            cookies.append(scraper[1])

    return name.groups()[0]


cookies = None


if __name__ == '__main__':
    print('Don\'t run this, please!')
