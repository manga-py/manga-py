#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json

domainUri = 'http://www.zingbox.me'


def get_main_content(url, get=None, post=None):
    id = re.search('/manga/(?:[^/]+/)?(\d+)/', url)
    _ = {
        'url': '/manga/getBookDetail/{}'.format(id.groups()[0]),
        'method': 'GET',
        'api': '/mangaheatapi/web',
    }
    return post(domainUri + '/api', data=_)


def get_volumes(content=None, url=None, get=None, post=None):
    try:
        return json.loads(content)['child']
    except Exception:
        return []


def get_archive_name(volume, index: int = None):
    return '{:0>3}'.format(volume['title'])


def get_images(main_content=None, volume=None, get=None, post=None):
    _ = {
        'url': '/manga/getChapterImages/{}'.format(volume['chapterId']),
        'method': 'GET',
        'api': '/mangaheatapi/web',
    }
    images = post(domainUri + '/api', data=_)
    return json.loads(images)['images']


def get_manga_name(url, get=None):
    name = re.search('\.me/manga/(?:\d+/)?([^/]+)', url)
    if not name:
        return ''
    return name.groups()[0].replace('+', ' ')


if __name__ == '__main__':
    print('Don\'t run this, please!')
