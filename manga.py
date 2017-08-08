#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import tempfile
import shutil
import atexit
import requests
import zipfile
from sys import stderr
from argparse import ArgumentParser
from urllib.parse import urlparse
from urllib import (
    request as url_request,
    error as url_error
)

# TODO: move import to providers/__init__.py
# @link: https://docs.python.org/3/reference/import.html
from providers import (
    desu_me,
    readmanga_me,
    shakai_ru,
    mangapanda_com,
    mintmanga_me,
    manga_online_biz,
    mangaclub_ru,
    ninemanga_com,
)
providers_list = (
    desu_me,
    readmanga_me,
    shakai_ru,
    mangapanda_com,
    mintmanga_me,
    manga_online_biz,
    mangaclub_ru,
    ninemanga_com,
)

user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36 OPR/44.0.2510.1218'

if os.name == 'nt':
    tty_rows = 0
    tty_columns = 0
else:
    tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

rnd_temp_path = str(random.random())
archivesDir = os.path.join(os.getcwd(), 'manga')

info_mode = False
count_reties = 5

referrer_url = ''


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


def _progress(items_count: int, current_item: int):
    if tty_columns:
        columns = float(tty_columns)
        one_percent = float(columns)/float(items_count)
        current_position = int(float(current_item) * one_percent)
        text = ('▓' * current_position)
        text += (' ' * (int(columns) - current_position))
        print('\033[1A\033[9D%s' % (text, ), end='\n        \033[9D')


def _create_parser():
    """
    Arguments parser helper
    """
    parse = ArgumentParser()

    parse.add_argument('-u', '--url', type=str, required=False, help='Downloaded url', default='')
    parse.add_argument('-n', '--name', type=str, required=False, help='Manga name', default='')
    parse.add_argument('-d', '--destination', type=str, required=False, help='Destination folder', default=archivesDir)
    parse.add_argument('-i', '--info', action='store_const', required=False, const=True, default=False)

    return parse


def __requests(url: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data=None, method='get'):
    if not headers:
        headers = {}
    if not cookies:
        cookies = ()
    if not data:
        data = ()
    if 'User-Agent' not in headers:
        headers['User-Agent'] = user_agent
    if 'Referer' not in headers:
        headers['Referer'] = referrer_url
    response = getattr(requests, method)(url=url, headers=headers, cookies=cookies, data=data)
    ret = response.text
    if offset > 0:
        ret = ret[offset:]
    if maxlen > 0:
        ret = ret[:maxlen]
    return ret


def _get(url: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None):
    return __requests(url=url, offset=offset, maxlen=maxlen, headers=headers, cookies=cookies, method='get')


def _post(url: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data: dict = ()):
    return __requests(url=url, offset=offset, maxlen=maxlen, headers=headers, cookies=cookies, method='post', data=data)


def _safe_downloader(url, file_name):
    try:
        # TODO: http://readmanga.me/the_seven_deadly_sins_/vol5/33?mature=1#page=2: /static/800px-Censored.jpg WTF!
        if url.find('http') != 0:
            url = referrer_url + url
        r = url_request.Request(url)
        r.add_header('User-Agent', user_agent)
        r.add_header('Referer', referrer_url)
        response = url_request.urlopen(r)
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


class MangaDownloader:

    url = ''
    name = ''
    main_content = ''
    status = False
    provider = None

    def __init__(self, url: str, name: str = ''):
        self.url = url
        self.name = name
        self.switcher()
        if len(name) < 1:
            self.get_manga_name()
        self.make_manga_dir()

        global referrer_url
        ref = urlparse(url)
        referrer_url = '{}://{}'.format(ref.scheme, ref.netloc)

    def _get_destination_directory(self):
        return os.path.join(arguments.destination, self.name)

    def switcher(self):
        self.status = True

        i = 0

        for d in providers_list:
            if d.test_url(self.url):
                break
            i += 1

        if i >= len(providers_list):
            self.status = False
            return

        self.provider = providers_list[i]

    def make_manga_dir(self):
        path = self._get_destination_directory().rstrip('/')
        if os.path.isdir(path):
            return
        try:
            os.makedirs(path)
        except NotADirectoryError:
            print('Destination not exist or not directory! Exit')
            exit(1)

    def get_manga_name(self):
        """
        получает название манги из url
        :param url:
        :return:
        """
        if self.status:
            self.name = self.provider.get_manga_name(self.url, get=_get)

    def get_main_content(self):
        """
        :return:
        """
        self.main_content = self.provider.get_main_content(self.url, get=_get, post=_post)

    def get_volumes(self):
        volumes = self.provider.get_volumes(self.main_content, url=self.url)
        return volumes

    def get_archive_destination(self, archive_name: str):
        d = os.path.join(self._get_destination_directory(), archive_name + '.zip')
        directory = os.path.dirname(d)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return d

    def get_images(self, volume):
        """
        :return:
        """
        images = self.provider.get_images(main_content=self.main_content, volume=volume, get=_get, post=_post)
        if info_mode and len(images) < 1:
            print('Images not found')
        return images

    def make_archive(self, archive_name: str):
        d = self.get_archive_destination(archive_name)
        archive = zipfile.ZipFile(d, 'w', zipfile.ZIP_DEFLATED)

        temp_directory = get_temp_path()
        for f in os.listdir(temp_directory):
            file = os.path.join(temp_directory, f)
            if os.path.isfile(file):
                archive.write(file, f)
        archive.close()

    def __download_image(self, url, path):
        r = 0
        while r < count_reties:
            if _safe_downloader(url, path):
                break
            if info_mode:
                mode = 'Skip image'
                if r < count_reties:
                    mode = 'Retry'
                print('Error downloading. %s' % (mode,))

    def __download_archive(self, url):
        archive_name = os.path.basename(url)
        if archive_name.find('.zip') > 0:
            archive_name = archive_name[:archive_name.find('.zip')]  # remove .zip
        dst = self.get_archive_destination(archive_name)
        if info_mode:
            print('Downloading archive: %s' % (archive_name,))
        self.__download_image(url, dst)

    def download_images(self):
        volumes = self.get_volumes()

        if getattr(self.provider, 'download_zip_only', False):
            if len(volumes):
                for v in volumes:
                    archive = self.provider.get_zip(volume=v, get=_get)
                    if archive is not str:
                        for i in archive:
                            self.__download_archive(i)
                    else:
                        self.__download_archive(archive)
            else:
                archives = self.provider.get_zip(main_content=self.main_content, get=_get)
                for a in archives:
                    self.__download_archive(a)
            return

        if len(volumes) < 1:
            print('Volumes not found. Exit')
            exit(1)

        volume_index = 1
        for v in volumes:
            temp_path = get_temp_path()
            archive_name = self.provider.get_archive_name(v, index=volume_index)
            volume_index += 1

            if not len(archive_name):
                if info_mode:
                    print('Archive name is empty!')
                exit(1)

            if os.path.isfile(self.get_archive_destination(archive_name)):
                if info_mode:
                    print('Archive %s exists. Skip' % (archive_name, ))
                continue

            images = self.get_images(v)

            if info_mode:
                print('Start downloading %s\n' % (archive_name, ))
            images_len = len(images)

            n = 1
            for i in images:
                if info_mode:
                    _progress(images_len, n)
                # hash name protected
                basename = '{:0>2}_{}'.format(n, os.path.basename(i))
                image_full_name = os.path.join(temp_path, basename)
                self.__download_image(i, image_full_name)
                n += 1

            self.make_archive(archive_name)
            shutil.rmtree(temp_path)


def manual_input(prompt: str):
    url = str(input(prompt + '\n'))
    if url == 'q':
        if info_mode:
            print('Quit command. Exit')
        exit(0)

    return url


def main(url: str, name: str = ''):
    if info_mode:
        print(url, name)
    manga = MangaDownloader(url, name)
    if manga.status:
        pass
        manga.get_main_content()
        manga.download_images()
    else:
        print('Status error. Exit')
        exit(1)

if __name__ == '__main__':
    arguments = _create_parser().parse_args()
    info_mode = arguments.info
    name = arguments.name
    if arguments.url:
        url = arguments.url
    else:
        url = manual_input('Please, paste manga url.')
        if len(name) < 1:
            name = manual_input('Please, paste manga name')
    main(url, name)
