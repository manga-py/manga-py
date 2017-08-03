#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import tempfile
import shutil
import atexit
from sys import stderr
from argparse import ArgumentParser
from urllib import (
    request as url_request,
    error as url_error
)
from requests import (
    get as get_request,
    post as post_request
)
from providers import (
    desu_me,
    readmanga_me,
    shakai_ru,
)
providers_list = (
    desu_me,
    readmanga_me,
    shakai_ru,
)

tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

rnd_temp_path = str(random.random())
archivesDir = os.path.join(os.getcwd(), 'manga')


if not os.path.isdir(archivesDir):
    if not os.access(os.getcwd(), os.W_OK):
        print('Current directory not writeable and manga directory not exist', file=stderr)
        exit(1)
    os.makedirs(archivesDir)
elif not os.access(archivesDir, os.W_OK):
    print('Manga directory not writable', file=stderr)
    exit(1)


@atexit.register
def before_shutdown():
    shutil.rmtree(get_temp_path())


def _progress(items_count: int = 0, current_item: int = 0):
    columns = int(tty_columns)
    one_percent = columns/items_count
    current_position = int(float(current_item) * one_percent)
    text = ('▓' * current_position)
    text += (' ' * (columns - current_position))
    print('\033[1A\033[9D%s' % (text, ), end='\n        \033[9D')


def _create_parser():
    """
    Arguments parser helper
    """
    parse = ArgumentParser()

    parse.add_argument('-u', '--url', type=str, required=False, help='Downloaded url', default='')
    parse.add_argument('-d', '--destination', type=str, required=False, help='Destination folder', default=archivesDir)

    return parse


def _get(filename: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None):
    if not headers:
        headers = {}
    if not cookies:
        cookies = ()
    response = get_request(filename, headers=headers, cookies=cookies)
    ret = response.text
    if offset > 0:
        ret = ret[offset:]
    if maxlen > 0:
        ret = ret[:maxlen]
    return ret


def _post(filename: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data: dict = ()):
    if not headers:
        headers = {}
    if not cookies:
        cookies = ()
    response = post_request(filename, headers=headers, cookies=cookies, data=data)
    ret = response.text
    if offset > 0:
        ret = ret[offset:]
    if maxlen > 0:
        ret = ret[:maxlen]
    return ret


def _safe_downloader(url, file_name):
    try:
        response = url_request.urlopen(url)
        out_file = open(file_name, 'wb')
        out_file.write(response.read())
        return True
    except url_error.HTTPError:
        return False
    except url_error.URLError:
        return False


def get_temp_path(path: str = ''):
    rnd_dir = os.path.join(tempfile.gettempdir(), rnd_temp_path)
    if not os.path.isdir(rnd_dir):
        os.makedirs(rnd_dir)
    return os.path.join(rnd_dir, path)


def get_content(uri: str):
    """
    :param uri:
    :return:
    """
    result = _get(uri)
    if result is None:
        return b''
    return result


class MangaDownloader:

    url = ''
    main_content = ''
    status = False
    downloader = None

    def __init__(self, url):
        self.url = url
        self.switcher()

    def switcher(self):
        self.status = True # if all ok

        i = 0

        if self.status:
            self.downloader = providers_list[i]

    def make_manga_dir(self, path):
        pass

    def get_manga_name(self):
        """
        получает название манги из url
        :param url:
        :return:
        """
        pass

    def get_main_content(self):
        """
        :param url:
        :return:
        """
        pass
        # return self.main_content # future

    def get_images(self):
        """
        :param url:
        :return:
        """
        return []

    def download_images(self, images: dict):
        pass


def manual_input():
    print('Please, paste desu.me manga url.')
    url = str(input())
    if url == 'q':
        print('Quit command. Exit')
        exit(0)


def main(url):
    manga = MangaDownloader(url)
    if manga.status:
        pass
        # manga.get_main_content()
        # manga.get_manga_name()
        # manga.make_manga_dir()
        # manga.get_images()

if __name__ == '__main__':
    arguments = _create_parser().parse_args()
    # print(arguments.destination, )
    # exit()
    if arguments.url:
        url = arguments.url
    else:
        url = manual_input()
    main(url)

    pass
