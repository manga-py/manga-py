#!/usr/bin/python3
# -*- coding: utf-8 -*-

if __file__.find('helpers/inmanga_com.py') < 0:
    print('Please run from the parent directory')
    exit()

from json import loads
from requests import get
from os import system


all_manga_list = None
n = 0
while n < 10:
    try:
        all_manga_list = loads(get('http://inmanga.com/OnMangaQuickSearch/Source/QSMangaList.json').text)
        break
    except Exception:
        pass
    n += 1
if not all_manga_list:
    print('Error! QSMangaList is not correct json?')

for i in all_manga_list:
    print('Downloading %s' % i['Name'])
    system('cd ../; python3 manga.py -p -i -u http://inmanga.com/ver/manga/{}/{}'.format(i['Name'], i['Name'], i['Identification']))
