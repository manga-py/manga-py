#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.cloudflare_scrape import cfscrape

domainUri = 'http://www.mangago.me'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/read-manga/{}/'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('#chapter_table a.chico')
    if parser is None:
        return []
    return [i.get('href') for i in parser]


def get_archive_name(volume, index: int = None):
    parser = re.search('read\-manga/[^/]+/[^/]+/(c\d+)/', volume)
    if not parser:
        return 'vol_{}'.format(index)
    return parser.groups()[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    parser = re.search("imgsrcs.+[^.]+?var.+?=\s?'(.+)'", content, re.M)
    if parser is None:
        return []
    imgs = parser.groups()[0]
    return imgs.split(',')


def get_manga_name(url, get=None):
    result = re.search('/read\-manga/([^/]+)/?', url)
    global cookies

    if not cookies:
        # anti-"cloudflare anti-bot protection"
        scraper = cfscrape.get_tokens(url)
        if scraper is not None:
            cookies = []
            for i in scraper[0]:
                cookies.append({
                    'value': scraper[0][i],
                    'domain': '.mangago.me',
                    'path': '/',
                    'name': i,
                })
            cookies.append(scraper[1])

    if not result:
        return ''
    return result.groups()[0]


cookies = None


if __name__ == '__main__':
    print('Don\'t run this, please!')
