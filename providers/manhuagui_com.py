#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
from helpers.main.crypt import manhuagui
import re
import json
import random

domainUri = 'http://www.manhuagui.com'

servers = [
    'i.hamreus.com:8080',
    'us.hamreus.com:8080',
    'dx.hamreus.com:8080',
    'eu.hamreus.com:8080',
    'lt.hamreus.com:8080',
]


def get_main_content(url, get=None, post=None):
    _id = re.search('/comic/(\d+)', url)
    if not _id:
        return ''
    return get('{}/comic/{}/'.format(domainUri, _id.groups()[0]))


def get_volumes(content=None, url=None, get=None, post=None):
    parser = document_fromstring(content)
    chapters = parser.cssselect('.chapter-list li > a')
    if len(chapters) < 1:
        chapters = parser.cssselect('#__VIEWSTATE')[0].get('value')

        js = manhuagui('LZString.decompressFromBase64("' + chapters + '")', '<a></a>')
        chapters = document_fromstring(js).cssselect('.chapter-list li > a')

    return [domainUri + i.get('href') for i in chapters]


def get_archive_name(volume, index: int = None):
    idx = re.search('comic/\d+/(\d+)', volume)
    frm = 'vol_{:0>3}'

    if idx:
        frm += '_{}'.format(idx.groups()[0])

    return frm.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    content = get(volume)
    js = re.search('\](\(function\(.+\))\s?<', content)
    if not js:
        return []
    data = manhuagui(js.groups()[0], '')
    data = re.search('cInfo=(.+)\|\|', data)
    if not data:
        return []
    data = json.loads(data.groups()[0])

    images = []
    for i in data['files']:
        prior = 3
        ln = len(servers)
        server = int(random.random() * (ln + prior))
        server = 0 if server < prior else server - prior
        images.append('http://{}{}{}'.format(servers[server], data['path'], i))

    return images


def get_manga_name(url, get=None):

    content = get(url)

    selector = 'h1'
    if re.search('/comic/\d+/\d+\\.html', url):
        selector = 'h1 > a'

    _u = document_fromstring(content).cssselect(selector)

    return _u[0].text_content()
