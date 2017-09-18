#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'https://com-x.life'


def get_main_content(url, get=None, post=None):
    manga_id = re.search('\.life.+?(\d+)', url).groups()[0]
    links_url = domainUri + '/engine/mods/comix/listPages.php'
    _data = {
        'newsid': manga_id,
        'page': 1
    }
    links = []
    while True:
        content = post(links_url, data=_data, headers={'content-type': 'application/x-www-form-urlencoded'})
        result = document_fromstring(content).cssselect('.comix-list li > a:not([style])')
        if not len(result):
            break
        _data['page'] += 1
        links += [i.get('href') for i in result]
    return links


def get_volumes(content=None, url=None, get=None, post=None):
    return content


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    prefix = domainUri + '/comix/'
    content = get(domainUri + volume)
    images = re.search('comix_images.*?(\[.+?\])', content)
    if not images:
        return []
    images = json.loads(images.groups()[0].replace("'", '"'))
    return [prefix + i for i in images]


def get_manga_name(url, get=None):
    test = re.search('\.life/readcomix/.+\.html', url)
    if test:
        parser = document_fromstring(get(url)).cssselect('#dle-speedbar > a')
        url = '.life' + parser[0].get('href')
    href = re.search('\.life/\d+\-(.+)\.html', url)
    print(href)
    if not href:
        return ''
    return href.groups()[0]


if __name__ == '__main__':
    print('Don\'t run this, please!')
