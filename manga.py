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

_downloader_uri = 'https://github.com/yuru-yuri/Manga-Downloader'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'

if os.name == 'nt':
    tty_rows = 0
    tty_columns = 0
else:
    tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

rnd_temp_path = 'manga-donloader_{}'.format(random.random()*10)
archivesDir = os.path.join(os.getcwd(), 'manga')

info_mode = False
show_progress = False
add_name = True
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
    parse.add_argument('-s', '--skip-volumes', type=int, required=False, help='Skip volumes', default=0)
    parse.add_argument('--no-name', action='store_const', required=False, help='Don\'t added manga name to the path', const=True, default=False)
    parse.add_argument('--allow-webp', action='store_const', required=False, help='Allow downloading webp images', const=True, default=False)
    parse.add_argument('--reverse-downloading', action='store_const', required=False, help='Reverse volumes downloading', const=True, default=False)
    parse.add_argument('--rewrite-exists-archives', action='store_const', required=False, const=True, default=False)

    return parse


def __requests(url: str, offset: int = -1, maxlen: int = -1, headers: dict=None, cookies: dict=None, data=None, method='get'):
    if not headers:
        headers = {}
    if not cookies:
        cookies = site_cookies
    if 'User-Agent' not in headers:
        headers['User-Agent'] = user_agent
    if arguments.allow_webp:
        headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
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
        if url.find('://') < 1:
            if url.find('/') == 0:
                _url = urlparse(referrer_url)
                _url = '{}://{}'.format(_url.scheme, _url.netloc)
            else:
                _url = referrer_url
            url = _url + url

        if not cookies:
            cookies = site_cookies

        response = requests.get(url, cookies=cookies, headers={
            'User-Agent': user_agent,
            'Referer': referrer_url
        })

        out_file = open(file_name, 'wb')
        out_file.write(response.content)
        return True
    except OSError:
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
        if add_name and len(name) < 1:
            self.get_manga_name()
        self.make_manga_dir()

        global referrer_url
        ref = urlparse(url)
        referrer_url = '{}://{}'.format(ref.scheme, ref.netloc)
        self._get_cookies(referrer_url)

    def _get_destination_directory(self):
        if not add_name:
            return arguments.destination
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
        volumes = self.provider.get_volumes(self.main_content, url=self.url)
        if not arguments.reverse_downloading:
            volumes.reverse()
        if arguments.skip_volumes > 0:
            return volumes[arguments.skip_volumes:]
        return volumes

    def get_archive_destination(self, archive_name: str):
        if archive_name.find('?') > 0:
            archive_name = archive_name[0:archive_name.find('?')]
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
        archive.writestr('info.txt', 'Site: {}\nDownloader: {}'.format(self.url, _downloader_uri))
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

    def __archive_helper(self, archive):
        n = 0
        if arguments.reverse_downloading:
            archive.reverse()
        if arguments.skip_volumes > 0:
            archive = archive[arguments.skip_volumes:]
        for a in archive:
            self.__download_archive(a)
            n += 1


    def download_images(self):
        volumes = self.get_volumes()

        if getattr(self.provider, 'download_zip_only', False):
            if len(volumes):
                for v in volumes:
                    archive = self.provider.get_zip(volume=v, get=_get, post=_post)
                    self.__archive_helper(archive)
            else:
                archive = self.provider.get_zip(main_content=self.main_content, get=_get, post=_post)
                self.__archive_helper(archive)
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

            if not arguments.rewrite_exists_archives and os.path.isfile(self.get_archive_destination(archive_name)):
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
                name = os.path.basename(i)
                if name.find('?') > 0:
                    name = name[0:name.find('?')]
                basename = '{:0>3}_{}'.format(n, name)
                if name.find('?') == 0 or len(name) < 4 or name.find('.') < 1:
                    basename = '{:0>3}.png'.format(n)
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
        add_name = not arguments.no_name
        name = arguments.name
        if arguments.url:
            url = arguments.url
        else:
            url = manual_input('Please, paste manga url.')
            if add_name and len(name) < 1:
                name = manual_input('Please, paste manga name')
        main(url, name)
    except KeyboardInterrupt:
        print('\033[84DUser interrupt this. Exit\t\t')
        exit(0)
