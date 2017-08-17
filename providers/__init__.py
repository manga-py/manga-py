#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

providers_list = {
    'desu_me': 'desu\.me/manga/.+?',
    'heymanga_me': 'heymanga\.me/manga/.+?',
    'manga_online_biz': 'manga\-online\.biz/.+',
    'mangaclub_ru': 'mangaclub\.ru/.+',
    'mangafox_me': 'mangafox\.me/manga/.+',
    'mangafreak_net': 'mangafreak\.net/.+',  # with cf-protect
    'mangago_me': 'mangago\.me/read\-manga/.+',  # with cf-protect
    'mangahere_co': 'mangahere\.co/manga/.+',
    'mangahome_com': 'mangahome\.com/manga/.+',
    'mangahub_ru': 'mangahub\.ru/.+',

    # doubles /*
    'mangakakalot_com': 'mangakakalot\.com/(manga|chapter)/.+',
    'manganel_com': 'manganel\.com/(manga|chapter)/.+',
    # */ doubles

    'mangaonlinehere_com': 'mangaonlinehere\.com/manga\-info/.+',
    'mangapanda_com': 'mangapanda\.com/.+',
    'mangapark_me': 'mangapark\.me/manga/.+',
    'mangareader_net': 'mangareader\.net/.+',
    'mangarussia_com': 'mangarussia\.com/manga.+',
    'mangatan_net': 'mangatan\.net/(manga|chapter).+',
    'mangatown_com': 'mangatown\.com/manga.+',
    'mintmanga_me': 'mintmanga\.me/.+',
    'ninemanga_com': 'ninemanga\.com/manga.+',
    'readmanga_me': 'readmanga\.me/.+',
    'selfmanga_ru': 'selfmanga\.ru/.+',
    'shakai_ru': 'shakai\.ru/manga.*?/\d+',
    'yagami_me': 'read\.yagami\.me/.+',
    'yaoichan_me': 'yaoichan\.me/(?:manga|online).+',
    'zingbox_me': 'zingbox\.me/.+',
}


def get_provider(url):
    for i in providers_list:
        result = re.search(providers_list[i], url)
        if result is not None:
            return __import__('providers.{}'.format(i), fromlist=['providers'])
    return False


if __name__ == '__main__':
    print('Don\'t run this, please!')
