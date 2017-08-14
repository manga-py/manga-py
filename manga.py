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
    error as url_error
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
show_progress = False
count_reties = 5

referrer_url = ''
site_cookies = ()


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
    parse.add_argument('-p', '--progress', action='store_const', required=False, const=True, default=False)

    return parse


def __requests(url: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data=None, method='get'):
    if not headers:
        headers = {}
    if not cookies:
        cookies = site_cookies
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


def _safe_downloader(url, file_name, cookies=None):
    try:
        # TODO: http://readmanga.me/the_seven_deadly_sins_/vol5/33?mature=1#page=2: /static/800px-Censored.jpg WTF!
        if url.find('://') < 1:
            url = referrer_url + url

        if not cookies:
            cookies = site_cookies

        response = requests.get(url, cookies=cookies, headers={
            'User-Agent': user_agent,
            'Referer': referrer_url
        })

        out_file = open(file_name, 'wb')
        out_file.write(response.content)
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
        self._get_cookies(referrer_url)

    def _get_destination_directory(self):
        return os.path.join(arguments.destination, self.name)

    def _get_cookies(self, url: str):
        session = requests.Session()
        h = session.head(url)
        global site_cookies
        if self.status and hasattr(self.provider, 'cookies') and getattr(self.provider, 'cookies'):
            cookies = getattr(self.provider, 'cookies')
            for i in cookies:
                if isinstance(i, str):
                    global user_agent
                    user_agent = i
                else:
                    h.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
        site_cookies = h.cookies

    def switcher(self):
        self.status = True

        import providers
        __p = providers.get_provider(self.url)

        if not __p:
            self.status = False
            return False

        self.provider = __p

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
        if self.status:
            self.name = self.provider.get_manga_name(self.url, get=_get)

    def get_main_content(self):
        self.main_content = self.provider.get_main_content(self.url, get=_get, post=_post)

    def get_volumes(self):
        return self.provider.get_volumes(self.main_content, url=self.url)

    def get_archive_destination(self, archive_name: str):
        d = os.path.join(self._get_destination_directory(), archive_name + '.zip')
        directory = os.path.dirname(d)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return d

    def get_images(self, volume):
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
                return True
            if info_mode:
                mode = 'Skip image'
                if r < count_reties:
                    mode = 'Retry'
                print('Error downloading. %s' % (mode,))
        return False

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
                print('Start downloading %s' % (archive_name, ))
            images_len = len(images)

            n = 1
            c = 0
            if show_progress:
                print('')
            for i in images:
                if show_progress:
                    _progress(images_len, n)
                # hash name protected
                basename = '{:0>2}_{}'.format(n, os.path.basename(i))
                image_full_name = os.path.join(temp_path, basename)
                if self.__download_image(i, image_full_name):
                    c += 1
                n += 1

            if c > 0:
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
    manga = MangaDownloader(url, name)
    if manga.status:
        pass
        manga.get_main_content()
        manga.download_images()
    else:
        print('Status error. Exit')
        exit(1)

if __name__ == '__main__':
    try:
        arguments = _create_parser().parse_args()
        info_mode = arguments.info
        show_progress = arguments.progress
        name = arguments.name
        if arguments.url:
            url = arguments.url
        else:
            url = manual_input('Please, paste manga url.')
            if len(name) < 1:
                name = manual_input('Please, paste manga name')
        main(url, name)
    except KeyboardInterrupt:
        print('\033[84DUser interrupt this. Exit\t\t')
        exit(0)
