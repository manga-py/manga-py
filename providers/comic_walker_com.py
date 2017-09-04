#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://comic-walker.com'
apiUri = 'https://cnts.comic-walker.com/api4js/v1/c'

_content = None
title = ''


def get_main_content(url, get=None, post=None):
    if not _content:
        get_manga_name(url)
    return _content


def get_volumes(content=None, url=None, get=None, post=None):
    items = document_fromstring(content).cssselect('.readableLinkColor')
    return [domainUri + i.get('href') for i in items]


def get_archive_name(volume, index: int = None):
    return 'vol_{:0>3}'.format(index)


def _image_helper(url, get, post):
    pass


def get_images(main_content=None, volume=None, get=None, post=None):
    # /KDCW_EB00000021010001_68?BID=150417983087600661690NFBR&AID=browser&AVER=1.2.0&FORMATS=epub_brws%2Cepub_brws_fixedlayout%2Cepub_brws_omf
    #
    pass


def get_manga_name(url, get=None):
    global _content
    global title
    if not _content:
        _content = get(url)
    if not len(title):
        name = document_fromstring(_content).cssselect('#mainContent h1')
        title = name[0].text_content()
    return title



if __name__ == '__main__':
    print('Don\'t run this, please!')
