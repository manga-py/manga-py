#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
# http://read.yagami.me/series/kubera/

domainUri = 'http://read.yagami.me'
uriRegex = '\\.me/(?:series|read)/([^/]+)/?'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/series/{}'.format(domainUri, name)
    return get(url)


def fix_volume_url(volume):
    # http://read.yagami.me/read/school_shock/0/1/0/rikudou_senin_clan/
    result = re.search(uriRegex + '(\d+/\d+/?\d*/)', volume)
    if not result:
        return volume
    _ = result.groups()
    return 'http://read.yagami.me/read/{}/{}page/1'.format(_[0], _[1])


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content).cssselect('#midside .list .element .title a')
    if not parser:
        return []
    return [fix_volume_url(i.get('href')) for i in parser]


def get_archive_name(volume, index: int = None):
    result = re.search('/read/.+?/(\d+/\d+)(/\d+)?/', volume)
    if not result:
        return 'vol_{}'.format(index)
    _ = result.groups()
    if _[1] is not None:
        return '{}_{}'.format(_[0], _[1].lstrip('/'))
    return _[0]


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    result = re.search('pages\s?=\s?(\[\{.+\}\])', content)
    if result is not None:
        result = json.loads(result.groups()[0])
        return [i['url'] for i in result]
    # other images (http://read.yagami.me/read/tower_of_god/)
    result = document_fromstring(content)
    images = result.cssselect('.web_pictures img.web_img')
    if images is not None and len(images) > 0:
        return [i.get('src') for i in images]
    return []


def get_manga_name(url, get=None):
    result = re.search(uriRegex, url).groups()
    return result[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
