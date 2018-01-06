#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json
from helpers.exceptions import UrlParseError

api_uri = 'https://api.mangarockhd.com/query/web400/info?oid={}&last=0&country='
api_content = ''


def _api_content(url, get):
    name = re.search('/manga/([^/]+)', url).group(1)
    global api_content
    if not len(api_content):
        api_content = get(api_content % name)
    return json.loads(api_content)


def get_main_content(url, get=None, post=None):
    return _api_content(url, get)


def get_volumes(content=None, url=None, get=None, post=None):
    return content['chapters']


def get_archive_name(volume, index: int = None):
    return '{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    # TODO
    pass


def get_manga_name(url, get=None):
    return _api_content(url, get)['name']
