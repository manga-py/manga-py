#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
import random
import tempfile
import shutil
import atexit
import requests
from requests.exceptions import TooManyRedirects
import zipfile
from sys import exc_info, stderr
from argparse import ArgumentParser
from urllib.parse import urlparse
from helpers import remove_void
from helpers.exceptions import *

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'
__version__ = '0.2.1.0'


_downloader_uri = 'https://github.com/yuru-yuri/Manga-Downloader'
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'

if os.name == 'nt':
    tty_rows = 0
    tty_columns = 0
else:
    tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

rnd_temp_path = 'manga-donloader_{}'.format(random.random()*10)
archivesDir = os.path.join(os.getcwd(), 'manga')

count_retries = 5

referrer_url = ''
site_cookies = ()


def _arguments_parser():  # pragma: no cover
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
    parse.add_argument('--max-volumes', type=int, required=False, help='Maximum volumes for downloading 0=All', default=0)
    parse.add_argument('--user-agent', required=False, type=str, default='')
    parse.add_argument('--no-name', action='store_const', required=False, help='Don\'t added manga name to the path', const=True, default=False)
    parse.add_argument('--allow-webp', action='store_const', required=False, help='Allow downloading webp images', const=True, default=False)
    parse.add_argument('--reverse-downloading', action='store_const', required=False, help='Reverse volumes downloading', const=True, default=False)
    parse.add_argument('--rewrite-exists-archives', action='store_const', required=False, const=True, default=False)

    parse.add_argument('-xt', required=False, type=int, help='Manual image crop with top side', default=0)
    parse.add_argument('-xr', required=False, type=int, help='Manual image crop with right side', default=0)
    parse.add_argument('-xb', required=False, type=int, help='Manual image crop with bottom side', default=0)
    parse.add_argument('-xl', required=False, type=int, help='Manual image crop with left side', default=0)

    parse.add_argument('--crop-blank', action='store_const', required=False, help='Crop white lines on image', const=True, default=False)
    parse.add_argument('--crop-blank-factor', required=False, type=int, help='Find factor 0..255. Default: 100', default=100)
    parse.add_argument('--crop-blank-max-size', required=False, type=int, help='Maximum crop size (px). Default: 30', default=30)

    return parse



@atexit.register
def before_shutdown():
    shutil.rmtree(get_temp_path())


def get_temp_path(path: str = ''):
    rnd_dir = os.path.join(tempfile.gettempdir(), rnd_temp_path)
    if not os.path.isdir(rnd_dir):
        os.makedirs(rnd_dir)
    return os.path.join(rnd_dir, path)


class VariablesHelper:

    url = ''
    name = ''
    main_content = ''
    status = False
    provider = None


class RequestsHelper(VariablesHelper):

    @staticmethod
    def __safe_downloader_url_helper(url):
        if url.find('//') == 0:
            return 'http:' + url
        if url.find('://') < 1:
            _ = referrer_url
            if url.find('/') == 0:
                _ = urlparse(referrer_url)
                _ = '{}://{}'.format(_.scheme, _.netloc)
            return _ + url
        return url

    # fast fixed #5
    def __requests_helper(self, method, url, headers=None, cookies=None, data=None, files=None, max_redirects=10):
        r = getattr(requests, method)(url=url, headers=headers, cookies=cookies, data=data, files=files, allow_redirects=False)
        if r.is_redirect:
            if max_redirects < 1:
                raise TooManyRedirects('Too many redirects', response=r)
            return self.__requests_helper(method, r.headers['location'], headers, cookies, data, files, max_redirects-1)
        return r

    def __requests(self, url: str, headers: dict=None, cookies: dict=None, data=None, method='get', files=None):
        if not headers:
            headers = {}
        if not cookies:
            cookies = site_cookies
        headers.setdefault('User-Agent', user_agent)
        headers.setdefault('Referer', referrer_url)
        if arguments.allow_webp:
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return self.__requests_helper(method=method, url=url, headers=headers, cookies=cookies, data=data, files=files)

    def _get(self, url: str, headers: dict=None, cookies: dict=None, offset: int = -1, maxlen: int = -1):
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='get')
        ret = response.text
        response.close()
        if offset > 0:
            ret = ret[offset:]
        if maxlen > 0:
            ret = ret[:maxlen]
        return ret

    def _post(self, url: str, headers: dict=None, cookies: dict=None, data: dict = (), files=None):
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='post', data=data, files=files)
        text = response.text
        response.close()
        return text

    def _safe_downloader(self, url, file_name):
        try:
            url = self.__safe_downloader_url_helper(url)
            response = self.__requests(url, method='get')

            with open(file_name, 'wb') as out_file:
                out_file.write(response.content)
            response.close()
            return True
        except OSError:
            return False

    def _get_cookies(self, url: str):
        session = requests.Session()
        h = session.head(url)
        global site_cookies
        cookies_exists = hasattr(self.provider, 'cookies') and getattr(self.provider, 'cookies')
        if self.status and cookies_exists:
            cookies = getattr(self.provider, 'cookies')
            for i in cookies:
                if isinstance(i, str):
                    global user_agent
                    user_agent = i
                else:
                    h.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
        session.close()
        site_cookies = h.cookies


class ImageHelper:

    @staticmethod
    def _crop_image(path):  # pragma: no cover
        name_without_ext = path[0:path.rfind('.')]
        ext = path[path.rfind('.'):]
        _path = os.path.join(os.path.dirname(path), '{}_{}'.format(name_without_ext, ext))
        cropper = remove_void.Cropper(path)
        result = cropper.process(_path, int(arguments.crop_blank_factor), int(arguments.crop_blank_max_size))
        if result:
            shutil.move(_path, path)
        else:
            os.unlink(_path)

    @staticmethod
    def _crop_manual(patch):  # pragma: no cover
        cropper = remove_void.Cropper(patch)
        cropper.crop({
            'left': arguments.xl,
            'top': arguments.xt,
            'bottom': arguments.xb,
            'right': arguments.xr,
        })


class MangaDownloader(RequestsHelper, ImageHelper):

    @staticmethod
    def _progress(items_count: int, current_item: int):  # pragma: no cover
        if arguments.progress and tty_columns:
            columns = float(tty_columns)
            one_percent = float(columns) / float(items_count)
            current_position = int(float(current_item) * one_percent)
            text = ('▓' * current_position)
            text += (' ' * (int(columns) - current_position))
            MangaDownloader.print('\033[1A\033[9D%s' % (text,), end='\n        \033[9D')

    @staticmethod
    def print(text, *args, **kwargs):
        __encode = 'utf-8'
        if os.name == 'nt':  # patch for issue #2 #6
            __encode = 'cp866'
        print(str(text).encode().decode(__encode, 'ignore'), *args, **kwargs)

    @staticmethod
    def print_info(text, *args, **kwargs):  # pragma: no cover
        if arguments.info:
            MangaDownloader.print(text, *args, **kwargs)

    @staticmethod
    def prepare_file_name(name):
        for i in '*|\\:"><?/':
            name = name.replace(i, '')
        return name

    @staticmethod
    def _download_image_name_helper(temp_path, i, n):
        name = os.path.basename(i)
        if name.find('?') > 0:
            name = name[0:name.find('?')]
        basename = '{:0>3}_{}'.format(n, name)
        name_question = name.find('?') == 0
        name_len = len(name) < 4
        name_dot = name.find('.') < 1
        if name_question or name_len or name_dot:
            basename = '{:0>3}.png'.format(n)
        return os.path.join(temp_path, basename)

    def __init__(self, url: str, name: str = ''):
        self.url = url
        self.name = name
        self.__switcher()
        if add_name and len(name) < 1:
            self.name = self.provider.get_manga_name(self.url, get=self._get)
        self._make_manga_dir()

        global referrer_url
        ref = urlparse(url)
        referrer_url = '{}://{}'.format(ref.scheme, ref.netloc)
        self._get_cookies(referrer_url)

    def _download_image(self, url, path):
        r = 0
        while r < count_retries:
            if self._safe_downloader(url, path):
                return True
            mode = 'Skip image'
            if r < count_retries:
                mode = 'Retry'
            MangaDownloader.print_info('Error downloading. %s' % (mode,))
        return False

    def __download_archive(self, url):
        archive_name = os.path.basename(url)
        if archive_name.find('.zip') > 0:
            archive_name = archive_name[:archive_name.find('.zip')]  # remove .zip
        dst = self._get_archive_destination(archive_name)
        MangaDownloader.print_info('Downloading archive: %s' % (archive_name,))
        self._download_image(url, dst)

    def _archive_helper(self, archive):
        n = 0
        if arguments.reverse_downloading:
            archive.reverse()
        if arguments.skip_volumes > 0:
            archive = archive[arguments.skip_volumes:]
        if arguments.max_volumes > 0:
            archive = archive[:arguments.max_volumes]
        for a in archive:
            self.__download_archive(a)
            n += 1
        return n

    def _download_zip_only(self, volumes):
        n = 0
        if len(volumes):
            for v in volumes:
                archive = self.provider.get_zip(volume=v, get=self._get, post=self._post)
                n += self._archive_helper(archive)
        else:
            archive = self.provider.get_zip(main_content=self.main_content, get=self._get, post=self._post)
            n += self._archive_helper(archive)
        if n < 1:
            raise VolumesNotFound('Volumes not found. Exit')

    def _download_images(self, images, archive_name, temp_path):

        MangaDownloader.print_info('Start downloading %s' % (archive_name,))
        images_len = len(images)

        n = 1
        c = 0
        if arguments.progress:
            MangaDownloader.print('')

        for i in images:

            self._progress(images_len, n)

            image_full_name = self._download_image_name_helper(temp_path, i, n)

            if self._download_image(i, image_full_name):
                c += 1

                self._crop_manual(image_full_name)

                if arguments.crop_blank:
                    self._crop_image(image_full_name)

            n += 1
        return c

    def _make_archive(self, archive_name: str):
        d = self._get_archive_destination(archive_name)
        archive = zipfile.ZipFile(d, 'w', zipfile.ZIP_DEFLATED)

        MangaDownloader.print_info('Make archive')

        temp_directory = get_temp_path()
        for f in os.listdir(temp_directory):
            file = os.path.join(temp_directory, f)
            if os.path.isfile(file):
                archive.write(file, f)
        archive.writestr('info.txt', 'Site: {}\nDownloader: {}'.format(self.url, _downloader_uri))
        archive.close()

    def _download_images_helper(self, v, volume_index):

        temp_path = get_temp_path()
        archive_name = self.provider.get_archive_name(v, index=volume_index)
        archive_name = self.prepare_file_name(archive_name)

        if not len(archive_name):
            raise VolumesNotFound('Archive name is empty!')

        if not arguments.rewrite_exists_archives and os.path.isfile(self._get_archive_destination(archive_name)):
            MangaDownloader.print_info('Archive %s exists. Skip' % (archive_name,))
            return False

        images = self._get_images(v)
        c = self._download_images(images, archive_name, temp_path)

        if c > 0:
            self._make_archive(archive_name)

        shutil.rmtree(temp_path)

    def __switcher(self):
        self.status = True

        import providers
        __p = providers.get_provider(self.url)

        if not __p:
            self.status = False
            return False

        self.provider = __p

    def _get_destination_directory(self):
        if not add_name:
            return arguments.destination
        return os.path.join(arguments.destination, self.name)

    def _make_manga_dir(self):
        path = self._get_destination_directory().rstrip('/')
        if os.path.isdir(path):
            return
        try:
            os.makedirs(path)
        except NotADirectoryError:
            raise DirectoryNotExists('Destination not exist or not directory! Exit')

    def get_main_content(self):
        self.main_content = self.provider.get_main_content(self.url, get=self._get, post=self._post)

    def _get_volumes(self):
        volumes = self.provider.get_volumes(self.main_content, url=self.url, get=self._get, post=self._post)
        if not arguments.reverse_downloading:
            volumes.reverse()
        if arguments.skip_volumes > 0:
            volumes = volumes[arguments.skip_volumes:]
        if arguments.max_volumes > 0:
            volumes = volumes[:arguments.max_volumes]
        return volumes

    def _get_archive_destination(self, archive_name: str):
        if archive_name.find('?') > 0:
            archive_name = archive_name[0:archive_name.find('?')]
        d = os.path.join(self._get_destination_directory(), archive_name + '.zip')
        directory = os.path.dirname(d)
        if not os.path.isdir(directory):
            os.makedirs(directory)
        return d

    def _get_images(self, volume):
        images = self.provider.get_images(main_content=self.main_content, volume=volume, get=self._get, post=self._post)
        if not len(images):
            MangaDownloader.print_info('Images not found')
        return images

    def download_images(self):
        volumes = self._get_volumes()

        if getattr(self.provider, 'download_zip_only', False):
            self._download_zip_only(volumes)
            return

        if len(volumes) < 1:
            raise VolumesNotFound('Volumes not found. Exit')

        volume_index = 1
        for v in volumes:
            self._download_images_helper(v, volume_index)
            volume_index += 1

    def main(self):
        self.get_main_content()
        self.download_images()


def manual_input(prompt: str):  # pragma: no cover
    url = str(input(prompt + '\n'))
    if url == 'q':
        MangaDownloader.print_info('Quit command. Exit')
        exit(0)

    return url


def main(url: str, name: str = ''):  # pragma: no cover
    manga = MangaDownloader(url, name)
    if manga.status:
        manga.main()
    else:
        raise StatusError('\nStatus error.\nProvider not found!\n Exit\n')


if __name__ == '__main__':  # pragma: no cover
    try:
        arguments = _arguments_parser().parse_args()
        add_name = not arguments.no_name
        name = arguments.name
        if len(arguments.user_agent):
            user_agent = arguments.user_agent

        if arguments.url:
            url = arguments.url
        else:
            url = manual_input('Please, paste manga url.')
            if add_name and len(name) < 1:
                name = manual_input('Please, paste manga name')
        try:
            main(url, name)
        except UrlParseError:
            MangaDownloader.print('Incorrect manga url.\nPlease, recheck url and report there on %s' % __email__)
        except (StatusError, DirectoryNotWritable, DirectoryNotExists, VolumesNotFound):
            MangaDownloader.print(exc_info()[1], file=stderr)
    except KeyboardInterrupt:
        MangaDownloader.print('\033[84DUser interrupt this. Exit\t\t')
        exit(0)
