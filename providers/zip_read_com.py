#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://zip-read.com'


def get_main_content(url, get=None, post=None):
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('#content .entry > p > a')
    return [i.get('href') for i in items]


def _get_jav_zip_id(uri):
    n = re.search('/\?p=(\d+)', uri)
    if not n:
        return 0
    return n.groups()[0]


def get_archive_name(volume, index: int = None):
    n = _get_jav_zip_id(volume)
    if n:
        return 'vol_{:0>3}_{}'.format(index, n)
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    if volume.find('jav-zip.org') > 0:
        images = []
        allow_more = True
        domain = 'http://jav-zip.org'
        step = 0
        _id = _get_jav_zip_id(volume)
        while allow_more:
            _uri = '{}/wp-admin/admin-ajax.php?post={}&action=get_content&step={}'
            content = json.loads(get(_uri.format(domain, _id, step)))
            content = document_fromstring(content['mes'])

            step += 50  # constant

            if len(content.cssselect('a.view-more')) < 1:
                allow_more = False

            for i in content.cssselect('img'):
                src = i.get('src')
                if src.find('http') != 0:
                    src = domain + src
                images.append(src)

        return images

    print('\nPlease, report this manga uri to sttv-pc@mail.ru\nThanks!\n')
    return []


def get_manga_name(url, get=None):
    name = re.search('.com/([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
