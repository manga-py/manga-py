#!/usr/bin/python3
# -*- coding: utf-8 -*-

import re

providers_list = {
    'bulumanga_com': 'bulumanga\.com/.+',
    # 'bwahahacomics_ru': 'bwahahacomics\.ru/.+',
    'bato_to': 'bato\.to/(comic|reader)/?.+',
    'com_x_life': 'com\-x\.life/.+\.html',
    # 'comic_walker_com': 'comic\-walker\.com/contents/detail/.+',
    'comico_jp': 'comico\.jp/(detail|articleList).+titleNo.+',
    'desu_me': 'desu\.me/manga/.+',
    'eatmanga_me': 'eatmanga\.me/.+',
    'funmanga_com': 'funmanga\.com/.+',
    'gogomanga_co': 'gogomanga\.co/.+',
    'goodmanga_net': 'goodmanga\.net/.+',
    'heymanga_me': 'heymanga\.me/manga/.+',
    'inmanga_com': 'inmanga\.com/ver/manga/.+',
    'jurnalu_ru': 'jurnalu\.ru/online\-reading/.+',
    'kissmanga_com': 'kissmanga\.com/Manga/.+',
    'manga_online_biz': 'manga\-online\.biz/.+',
    'manga_online_com_ua': 'manga\-online\.com\.ua/.+',
    'mangabb_co': 'mangabb\.co/.+',
    'mangabox_me': 'mangabox\.me/reader/.+',
    'mangachan_me': 'mangachan\.me/[^/]+/.+',
    'mangaclub_ru': 'mangaclub\.ru/.+',
    'mangaeden_com': 'mangaeden.com/[^/]+/[^/]+\-manga/.+',
    'mangafox_me': 'mangafox\.me/manga/.+',
    'mangafreak_net': 'mangafreak\.net/.+',  # with cf-protect
    'mangago_me': 'mangago\.me/read\-manga/.+',  # with cf-protect
    'mangahead_me': 'mangahead\.me/.*Manga-\w+-Scan/.+',
    'mangahere_co': 'mangahere\.co/manga/.+',
    'mangahome_com': 'mangahome\.com/manga/.+',
    'mangahub_ru': 'mangahub\.ru/.+',
    'mangainn_net': 'mangainn\.net/manga/.+',
    'mangakakalot_com': 'mangakakalot\.com/(manga|chapter)/.+',
    'mangaleader_com': 'mangaleader\.com/read\-.+',
    'mangalib_me': 'mangalib\.me/.+',
    'mangamove_com': 'mangamove\.com/manga/.+',
    'manganel_com': 'manganel\.com/(manga|chapter)/.+',
    'mangaonlinehere_com': 'mangaonlinehere\.com/manga\-info/.+',
    'mangapanda_com': 'mangapanda\.com/.+',
    'mangapark_me': 'mangapark\.me/manga/.+',
    'mangareader_net': 'mangareader\.net/.+',
    'mangarussia_com': 'mangarussia\.com/manga.+',
    'mangasaurus_com': 'mangasaurus\.com/manga.+',
    'mangasupa_com': 'mangasupa\.com/(manga|chapter).+',
    'mangatan_net': '(mangashin\.com|mangatan\.net)/(manga|chapter)',  # site renamed to mangashin.com
    'mangatown_com': 'mangatown\.com/manga.+',
    'manhuagui_com': 'manhuagui\.com/comic/\d+',
    'mintmanga_com': 'mintmanga\.com/.+',
    'myreadingmanga_info': 'myreadingmanga\.info/.+',  # with cf-protect
    'ninemanga_com': 'ninemanga\.com/manga.+',
    # 'onemanga_com': 'onemanga\.com/manga.+',
    'read_yagami_me': 'read\.yagami\.me/.+',
    'readmanga_me': 'readmanga\.me/.+',
    'selfmanga_ru': 'selfmanga\.ru/.+',
    'shakai_ru': 'shakai\.ru/manga.*?/\d+',
    'somanga_net': 'somanga\.net/.+',
    'tenmanga_com': 'tenmanga\.com/(book|chapter)/.+',
    'unixmanga_nl': 'unixmanga\.nl/onlinereading/.+\.html',
    'wmanga_ru': 'wmanga\.ru/starter/manga_.+',
    'yaoichan_me': 'yaoichan\.me/(manga|online).+',
    'zingbox_me': 'zingbox\.me/.+',
    'zip_read_com': 'zip\-read\.com/.+',
}


def get_provider(url):
    for i in providers_list:
        result = re.search(providers_list[i], url)
        if result is not None:
            return __import__('providers.{}'.format(i), fromlist=['providers'])
    return False


if __name__ == '__main__':
    print('Don\'t run this, please!')
