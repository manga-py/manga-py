#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json

domainUri = 'http://manga-online.biz'
nameRegex = '\\.biz/([^/]+)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}.html'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None, get=None, post=None):
    return []


def get_archive_name(volume, index: int = None):
    return ''


def get_images(main_content=None, volume=None, get=None, post=None):
    return []


def get_manga_name(url, get=None):
    test_name = re.search(nameRegex + '\\.html', url)
    if test_name:
        return test_name.groups()[0]
    return re.search(nameRegex, url).groups()[0]


download_zip_only = True


def get_zip(main_content=None, volume=None, get=None, post=None):

    result = re.search('MangaChapter\((\[.+\])\)', main_content)
    if result is not None:
        result = result.groups()[0].replace("'", '"')
        result = json.loads(result)
        result.reverse()
        return [domainUri + i['downloadUrl'] for i in result]
    return []


if __name__ == '__main__':
    print('Don\'t run this, please!')
