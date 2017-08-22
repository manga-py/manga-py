#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://shakai.ru'
nameRegex = 'file/manga/([a-zA-Z_]+)/(?:manga|cover)/([^/]+)/?'


def get_main_content(url, get=None, post=None):
    name = _get_manga_number(url)
    _ = {
        'dataRun': 'api-manga',
        'dataRequest': name
    }
    page_content = str(post('http://shakai.ru/take/api-manga/request/shakai', data=_))
    return page_content


def get_volumes(content, url=None):
    if not content:
        return []
    _ = json.loads(content)
    if not 'data' in _:
        return []
    volumes_links = _['data']
    volumes_links.reverse()
    return volumes_links


def get_archive_name(volume, index: int = None):
    if volume is not None and 'data-second' in volume:
        url = re.search(nameRegex, volume['data-second'][0])
        return url.groups()[1]
    return 'vol_{}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    if volume is not None and 'data-second' in volume:
        return volume['data-second']
    return []


def _get_manga_number(url):
    result = re.match('\.ru/manga(?:-read)?/(\d+)/?', url)
    if result is None:
        return ''
    result = result.groups()
    if not len(result):
        return ''
    return result[0]


def get_manga_name(url, get=None):
    content = get(url)
    parser = document_fromstring(content)
    result = parser.cssselect('.make__cover > img')

    if result is not None or len(result) > 0:
        src = re.search(nameRegex, result[0].get('src'))

        if src is not None:
            return src.groups()[0]

    return _get_manga_number(url)


if __name__ == '__main__':
    print('Don\'t run this, please!')
