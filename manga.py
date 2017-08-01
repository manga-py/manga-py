#!/usr/bin/python3
# -*- coding: utf-8 -*-

import desu_me
import readmanga_me
import shakai_ru

from requests import (get as get_request, post as post_request)
import lxml.html as html
import zipfile
from urllib import (
    request as url_request,
    error as url_error,
    parse
)
import tempfile
import os
import random
import re
import json
from sys import stderr
from shutil import (rmtree, move)

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

    def __init__(self, url):
        self.url = url

    # не перегружать.
    def switcher(self):
        pass

    def mkdir_manga_dir(self, path):
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
        return self.main_content

    def get_images(self):
        """
        :param url:
        :return:
        """
        return []

    def download_images(self, images: dict):
        pass


def main():
    pass

if __name__ == '__main__':
    main()
    rmtree(get_temp_path())
