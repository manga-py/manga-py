#!/usr/bin/python3
# -*- coding: utf-8 -*-

import atexit
import os
import random
import shutil
import tempfile
import zipfile
from argparse import ArgumentParser
from sys import exc_info, stderr
from threading import Thread
from urllib.parse import urlparse

import requests
from requests.exceptions import TooManyRedirects

from helpers import remove_void
from helpers.exceptions import *

__author__ = 'Sergey Zharkov'
__license__ = 'MIT'
__email__ = 'sttv-pc@mail.ru'
__version__ = '0.2.2.0'
__downloader_uri__ = 'https://github.com/yuru-yuri/Manga-Downloader'

if os.name == 'nt':
    tty_rows = 0
    tty_columns = 0
else:
    tty_rows, tty_columns = os.popen('stty size', 'r').read().split()

count_retries = 5
rnd_temp_path = 'manga-donloader_{}'.format(random.random()*10)
archivesDir = os.path.join(os.getcwd(), 'manga')
simulate_downloading = False


def _arguments_parser() -> ArgumentParser:  # pragma: no cover
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
    parse.add_argument('--no-multi-threads', action='store_const', required=False, help='Disallow multi-threads images downloading', const=True, default=False)

    parse.add_argument('-xt', required=False, type=int, help='Manual image crop with top side', default=0)
    parse.add_argument('-xr', required=False, type=int, help='Manual image crop with right side', default=0)
    parse.add_argument('-xb', required=False, type=int, help='Manual image crop with bottom side', default=0)
    parse.add_argument('-xl', required=False, type=int, help='Manual image crop with left side', default=0)

    parse.add_argument('--crop-blank', action='store_const', required=False, help='Crop white lines on image', const=True, default=False)
    parse.add_argument('--crop-blank-factor', required=False, type=int, help='Find factor 0..255. Default: 100', default=100)
    parse.add_argument('--crop-blank-max-size', required=False, type=int, help='Maximum crop size (px). Default: 30', default=30)

    parse.add_argument('--proxy', required=False, type=str, help='Http proxy', default='')

    return parse


@atexit.register
def before_shutdown():
    shutil.rmtree(get_temp_path())


def get_temp_path(path: str = '') -> str:
    rnd_dir = os.path.join(tempfile.gettempdir(), rnd_temp_path)
    if not os.path.isdir(rnd_dir):
        os.makedirs(rnd_dir)
    return os.path.join(rnd_dir, path)


class VariablesHelper:

    url = ''
    name = ''
    main_content = ''
    provider = None
    site_cookies = {}
    referrer_url = ''
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36'


class MultiThreads:

    threads = []

    def __init__(self):
        self.threads = []

    def addThread(self, target: callable, args: tuple):
        self.threads.append(Thread(target=target, args=args))

    def startAll(self):
        for t in self.threads:  # starting all threads
            t.start()
        for t in self.threads:  # joining all threads
            t.join()
        self.threads = []


class RequestsHelper(VariablesHelper):

    @staticmethod
    def remove_file_name_params(name, save_path: bool = True) -> str:
        file_path = os.path.dirname(name)
        name = os.path.basename(name)
        if name.find('?') > 0:
            name = name[0:name.find('?')]
        return os.path.join(file_path, name) if save_path else name

    def __safe_downloader_url_helper(self, url: str) -> str:
        if url.find('//') == 0:
            _ = urlparse(self.referrer_url)
            return _.scheme + ':' + url
        if url.find('://') < 1:
            _ = self.referrer_url[0:self.referrer_url.rfind('/')]
            if url.find('/') == 0:
                _ = urlparse(self.referrer_url)
                _ = '{}://{}'.format(_.scheme, _.netloc)
            return _.rstrip('/') + '/' + url.lstrip('/')
        return url

    # fast fixed #5
    def __requests_helper(self, method, url, headers=None, cookies=None, data=None, files=None, max_redirects=10, timeout=None, proxies=None) -> requests.Response:
        r = getattr(requests, method)(url=url, headers=headers, cookies=cookies, data=data, files=files, allow_redirects=False, proxies=proxies)
        if r.is_redirect:
            if max_redirects < 1:
                raise TooManyRedirects('Too many redirects', response=r)
            return self.__requests_helper(method, r.headers['location'], headers, cookies, data, files, max_redirects-1, timeout=timeout)
        return r

    def __requests(self, url: str, headers: dict=None, cookies: dict=None, data=None, method='get', files=None, timeout=None, proxies=None) -> requests.Response:
        if not headers:
            headers = {}
        if not cookies:
            cookies = self.site_cookies
        headers.setdefault('User-Agent', self.user_agent)
        headers.setdefault('Referer', self.referrer_url)
        if arguments.allow_webp:
            headers['Accept'] = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
        return self.__requests_helper(method=method, url=url, headers=headers, cookies=cookies, data=data, files=files, timeout=timeout, proxies=proxies)

    def _get(self, url: str, headers: dict=None, cookies: dict=None, offset: int = -1, maxlen: int = -1) -> str:
        proxies = None
        if hasattr(arguments, 'proxy') and arguments.proxy.find('http') == 0:
            proxies = {'http': arguments.proxy, 'https': arguments.proxy}
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='get', proxies=proxies)
        ret = response.text
        response.close()
        if offset > 0:
            ret = ret[offset:]
        if maxlen > 0:
            ret = ret[:maxlen]
        return ret

    def _post(self, url: str, headers: dict=None, cookies: dict=None, data: dict = (), files=None) -> str:
        proxies = None
        if hasattr(arguments, 'proxy') and arguments.proxy.find('http') == 0:
            proxies = {'http': arguments.proxy, 'https': arguments.proxy}
        response = self.__requests(url=url, headers=headers, cookies=cookies, method='post', data=data, files=files, proxies=proxies)
        text = response.text
        response.close()
        return text

    def _safe_downloader(self, url, file_name) -> bool:
        if url == -1:  # FIXME: viz.com crunch
            return True
        try:
            url = self.__safe_downloader_url_helper(url)
            response = self.__requests(url, method='get', timeout=3)

            with open(file_name, 'wb') as out_file:
                out_file.write(response.content)
                out_file.close()
            response.close()
            return True
        except OSError:
            return False

    def _prepare_cookies(self, url: str):
        session = requests.Session()
        h = session.head(url)
        cookies_exists = hasattr(self.provider, 'cookies') and getattr(self.provider, 'cookies')
        if cookies_exists:
            cookies = getattr(self.provider, 'cookies')
            for i in cookies:
                if isinstance(i, str):
                    self.user_agent = i
                else:
                    h.cookies.set(i['name'], i['value'], domain=i['domain'], path=i['path'])
        session.close()
        self.site_cookies = h.cookies


class ImageHelper:

    @staticmethod
    def _crop_image(path: str):  # pragma: no cover
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
    def _crop_manual(patch: str):  # pragma: no cover
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
            MangaDownloader.print('\033[1A\033[9D%s' % text, end='\n        \033[9D')

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
    def _download_image_name_helper(temp_path, i, n) -> str:
        name = RequestsHelper.remove_file_name_params(i, False)
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

        # FIXME: viz.com crunch
        setattr(self.provider, 'download_one_file', self.download_one_file)

        if len(arguments.user_agent):
            self.user_agent = arguments.user_agent

        ref = urlparse(url)
        self.referrer_url = '{}://{}'.format(ref.scheme, ref.netloc)
        self._prepare_cookies(self.referrer_url)

    def __simulate_downloading(self, path):
        with open(path, 'wb') as f:
            f.write(b'0')
            f.close()
        return True

    def __download_one_file_helper(self, url, dest):
        r = 0
        while r < count_retries:
            if self._safe_downloader(url, dest):
                return True
            mode = 'Skip image'
            if r < count_retries:
                mode = 'Retry'
            MangaDownloader.print_info('Error downloading. %s' % (mode,))
        return False

    def download_one_file(self, url: str, dest: str = None) -> bool:
        if not dest:
            name = os.path.basename(RequestsHelper.remove_file_name_params(url))
            dest = os.path.join(get_temp_path(), name)
        if simulate_downloading:
            self.__simulate_downloading(dest)
            return True
        return self.__download_one_file_helper(url, dest)

    def __download_archive(self, url: str):
        archive_name = os.path.basename(url)
        if archive_name.find('.zip') > 0:
            archive_name = archive_name[:archive_name.find('.zip')]  # remove .zip
        dst = self._get_archive_destination(archive_name)
        MangaDownloader.print_info('Downloading archive: %s' % (archive_name,))
        self.download_one_file(url, dst)

    def _archive_helper(self, archives: list):
        n = 0
        if arguments.reverse_downloading:
            archives.reverse()
        if arguments.skip_volumes > 0:
            archives = archives[arguments.skip_volumes:]
        if arguments.max_volumes > 0:
            archives = archives[:arguments.max_volumes]
        for a in archives:
            self.__download_archive(a)
            n += 1
        return n

    def _download_zip_only(self, volumes: list):
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

    def __one_thread_downloader(self, temp_path, image, n, callback: callable = None, callback_params=None):
        image_full_name = self._download_image_name_helper(temp_path, image, n)
        result = 0
        if self.download_one_file(image, image_full_name):
            self._crop_manual(image_full_name)
            if arguments.crop_blank:
                self._crop_image(image_full_name)
            result = 1

        if callback:
            callback(result, callback_params)
        return result

    def _download_images(self, images: list, archive_name: str, temp_path: str):

        MangaDownloader.print_info('Start downloading %s' % (archive_name,))
        images_len = len(images)

        n = 1
        _c = [0]
        if arguments.progress:
            MangaDownloader.print('')

        if not arguments.no_multi_threads:
            def thread_done(result, counter):
                counter[0] += result

            threads = MultiThreads()

            for i in images:
                threads.addThread(self.__one_thread_downloader, (temp_path, i, n, thread_done, _c))
                n += 1
            threads.startAll()

            return _c[0]
        else:
            for i in images:
                self._progress(images_len, n)
                _c[0] += self.__one_thread_downloader(temp_path, i, n)
                n += 1
        return _c[0]

    def _make_archive(self, archive_name: str):
        d = self._get_archive_destination(archive_name)
        archive = zipfile.ZipFile(d, 'w', zipfile.ZIP_DEFLATED)

        MangaDownloader.print_info('Make archive')

        temp_directory = get_temp_path()
        for f in os.listdir(temp_directory):
            file = os.path.join(temp_directory, f)
            if os.path.isfile(file):
                archive.write(file, f)
        archive.writestr('info.txt', 'Site: {}\nDownloader: {}'.format(self.url, __downloader_uri__))
        archive.close()

    def _download_images_helper(self, v: str, volume_index: int):

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

        import providers
        __p = providers.get_provider(self.url)

        if not __p:
            raise ProviderNotFound()

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
    try:
        manga = MangaDownloader(url, name)
        manga.main()
    except ProviderNotFound:
        MangaDownloader.print('\nStatus error.\nProvider not found!\n Exit\n')
    except UrlParseError:
        MangaDownloader.print('Incorrect manga url.\nPlease, recheck url and report there on %s' % __email__)
    except (StatusError, DirectoryNotWritable, DirectoryNotExists, VolumesNotFound):
        MangaDownloader.print(exc_info()[1], file=stderr)


if __name__ == '__main__':  # pragma: no cover
    try:
        arguments = _arguments_parser().parse_args()
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
        MangaDownloader.print('\033[84DUser interrupt this. Exit\t\t')
        exit(0)
