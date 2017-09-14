#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json

domainUri = 'http://bulumanga.com'
manga_id = 0
_content = ''


def _check_source(url, _id):
    source = re.search('source=(\w+)', url)
    resources = json.loads(_content)['sources']
    if source:
        source = source.groups()[0]
        for n, i in enumerate(resources):
            if i['source'] == source:
                return [_id, resources[n]]

    print('Please, select resource:')
    for n, i in enumerate(resources):
        print('{} - {}'.format(n+1, i['source']))

    while True:
        n = int(input())
        if len(resources) >= n > 0:
            return [_id, resources[n - 1]]
        print('Error. Please, select resource')


def get_main_content(url, get=None, post=None):
    global manga_id
    global _content

    _id = re.search('id=(\d+)', url).groups()[0]
    manga_id = _id

    if not len(_content):
        _url = '{}/detail/{}'.format(domainUri, _id)
        content = get(_url)
        _content = content

    return _check_source(url, _id)


def get_volumes(content=None, url=None, get=None, post=None):
    items = get('{}/detail/{}?source={}'.format(domainUri, content[0], content[1]['source']))
    items = json.loads(items)['chapters']
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    if not manga_id or 'cid' not in volume:
        return []
    content = json.loads(get('{}/page/mangareader/{}/{}'.format(domainUri, manga_id, volume['cid'])))
    return [i['link'] for i in content['pages']]


def get_manga_name(url, get=None):
    global _content

    if not len(_content):
        _id = re.search('id=(\d+)', url)
        if not _id:
            raise AttributeError('Manga id not found')
        _id = _id.groups()[0]
        _url = '{}/detail/{}'.format(domainUri, _id)
        content = get(_url)
        _content = content
    else:
        content = _content

    name = json.loads(content)['name']
    name = re.sub('[@$:/\\\]', '_', name)
    return name


if __name__ == '__main__':
    print('Don\'t run this, please!')
