#!/usr/bin/python3
# -*- coding: utf-8 -*-

from requests import get
from os import system, path
from lxml.html import document_fromstring

_path = path.dirname(path.dirname(path.realpath(__file__)))

all_manga_list = None
n = 0
base_path = 'http://animextremist.com/mangas-online/'
while n < 10:
    try:
        all_manga_list = document_fromstring(get(base_path)).cssselect('li > a + a')
        break
    except Exception:
        pass
    n += 1

for i in all_manga_list:
    href = i.get('href')
    print('Downloading %s' % href)
    _str = 'cd {}; python3 manga.py --cli -i -u {}'
    system(_str.format(_path, href))
