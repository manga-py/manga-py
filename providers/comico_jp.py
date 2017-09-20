#!/usr/bin/python3
# -*- coding: utf-8 -*-

from lxml.html import document_fromstring
import re
import json

domainUri = 'http://www.comico.jp'


def get_main_content(url, get=None, post=None):
    title_no = re.search('\.jp/.+titleNo=(\d+)', url)
    if title_no:
        content = post('{}/api/getArticleList.nhn'.format(domainUri), data={
            'titleNo': title_no.groups()[0]
        })
        try:
            return json.loads(content)['result']['list']
        except TypeError:
            pass
    return []


def get_volumes(content=None, url=None, get=None, post=None):
    # see i['freeFlg'] Y = true, W = false #19
    items = [i['articleDetailUrl'] for i in content]
    items.reverse()
    return items


def get_archive_name(volume, index: int = None):
    return '{:0>3}'.format(index)


def get_images(main_content=None, volume=None, get=None, post=None):
    items = document_fromstring(get(volume)).cssselect('.comic-image._comicImage > img.comic-image__image')
    return [i.get('src') for i in items]


def get_manga_name(url, get=None):
    name = document_fromstring(get(url)).cssselect('title')[0].text_content()
    name = name[:name.rfind('|')].strip(' \n\t\r')

    return name


if __name__ == '__main__':
    print('Don\'t run this, please!')
