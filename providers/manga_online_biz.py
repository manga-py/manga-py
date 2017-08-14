#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re
import json

domainUri = 'http://manga-online.biz'
nameRegex = 'https?://(?:www\.)?manga\-online\.biz/([^/]+)'
imagesRegex = 'MangaChapter\((\[.+\])\)'


def get_main_content(url, get=None, post=None):
    name = get_manga_name(url)
    url = '{}/{}.html'.format(domainUri, name)
    return get(url)


def get_volumes(content=None, url=None):
    return []


def get_archive_name(volume, index: int = None):
    return ''


def get_images(main_content=None, volume=None, get=None, post=None):
    return []


def get_manga_name(url, get=None):
    test_name = re.search(nameRegex + '\.html', url)
    if test_name is not None:
        return test_name.groups()[0]
    return re.search(nameRegex, url).groups()[0]


download_zip_only = True


def get_zip(main_content=None, volume=None, get=None, post=None):

    result = re.search(imagesRegex, main_content)
    if result is not None:
        result = result.groups()[0].replace("'", '"')
        result = json.loads(result)

        list = [domainUri + i['downloadUrl'] for i in result]
        list.reverse()
        return list
    return []


if __name__ == '__main__':
    print('Don\'t run this, please!')
