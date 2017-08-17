#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
from helpers.cloudflare_scrape import cfscrape

domainUri = 'http://www3.mangafreak.net'
uriRegex = '/Manga/([^/]+)/?'


def get_main_content(url, get=None, post=None):
    _ = '{}/Manga/{}'.format(domainUri, get_manga_name(url))
    return get(_)


def get_volumes(content=None, url=None):
    return []


def get_archive_name(volume, index: int = None):
    return ''


def get_images(main_content=None, volume=None, get=None, post=None):
    return []


def get_manga_name(url, get=None):
    # http://www3.mangafreak.net/Manga/Onepunch_Man
    # http://www3.mangafreak.net/Read1_Onepunch_Man_1

    # anti-"cloudflare anti-bot protection"
    scraper = cfscrape.get_tokens(url)
    global cookies
    if scraper is not None:
        cookies = []
        for i in scraper[0]:
            cookies.append({
                'value': scraper[0][i],
                'domain': '.mangafreak.net',
                'path': '/',
                'name': i,
            })
        cookies.append(scraper[1])

    test = re.search(uriRegex, url)
    if test:
        return test.groups()[0]
    test = re.search('/Read\d+_(.+)_\d+', url)
    if test:
        return test.groups()[0]
    return ''


download_zip_only = True


def get_zip(main_content=None, volume=None, get=None, post=None):
    links = document_fromstring(main_content).cssselect('.manga_series_list a[download]')
    return [i.get('href') for i in links]


cookies = None


if __name__ == '__main__':
    print('Don\'t run this, please!')
