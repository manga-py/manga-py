#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

providers_list = {
    'desu_me': 'desu\.me/manga/.+?',
    'manga_online_biz': 'manga\-online\.biz/.+',
    'mangaclub_ru': 'mangaclub\.ru/.+',
    'mangafreak_net': 'mangafreak\.net/.+',  # with cf-protect
    'mangago_me': 'mangago\.me/read\-manga/',  # with cf-protect
    'mangahub_ru': 'mangahub\.ru/.+',
    'mangapanda_com': 'mangapanda.com/.+',
    'mangarussia_com': 'mangarussia\.com/manga',
    'mintmanga_me': 'mintmanga\.me/.+',
    'ninemanga_com': 'ninemanga\.com/manga',
    'readmanga_me': 'readmanga\.me/.+',
    'selfmanga_ru': 'selfmanga\.ru/',
    'shakai_ru': 'shakai\.ru/manga.*?/\d+',
    'yagami_me': 'read\.yagami\.me/.+',
    'yaoichan_me': 'yaoichan\.me/(?:manga|online)',
}


def get_provider(url):
    for i in providers_list:
        result = re.search(providers_list[i], url)
        if result is not None:
            return __import__('providers.{}'.format(i), fromlist=['providers'])
    return False


if __name__ == '__main__':
    print('Don\'t run this, please!')
