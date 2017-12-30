import json
import re
from zipfile import ZipFile, ZIP_DEFLATED
from abc import abstractmethod, ABCMeta
from typing import Callable

from lxml.html import document_fromstring

from libs.fs import (
    get_temp_path,
    is_file,
    is_dir,
    make_dirs,
    basename,
    dirname,
    remove_file_query_params,
    path_join,
    unlink
)
from libs.http import Http
from libs.image import Image
from libs.cli import __version__, __downloader_uri__


class ChapterHelper:

    def __init__(self, chapters: str):
        self.chapters = chapters
        if isinstance(self.chapters, str):
            self.chapters = self.chapters.split(' ')

    def get_chapters(self, urls):
        chapters = []
        for i, url in enumerate(urls):
            if i in self.chapters:
                chapters.append(urls)
        return chapters


class AbstractProvider:

    @abstractmethod
    def get_main_content(self):  # call once
        pass

    @abstractmethod
    def get_manga_name(self) -> str:  # call once
        return ''

    @abstractmethod
    def get_chapters(self) -> list:  # call once
        return []

    @abstractmethod
    def get_cookies(self):  # if site with cookie protect
        pass

    @abstractmethod
    def get_files(self) -> list:  # call ever volume loop
        return []

    @abstractmethod
    def _loop_callback_volumes(self):
        pass

    @abstractmethod
    def _loop_callback_files(self):
        pass

    @abstractmethod
    def get_archive_name(self):
        pass


class BaseProvider:
    _storage = {
        'cookies': (),
        'main_content': '',
        'chapters': [],
        'current_chapter': 0,
        'current_file': 0
    }
    _params = {
        'path_destination': 'Manga'
    }

    @staticmethod
    def document_fromstring(body, selector: str = None, idx: int = None):
        result = document_fromstring(body)
        if isinstance(selector, str):
            result = result.cssselect(selector)
        if isinstance(idx, int):
            result = result[abs(idx)]
        return result

    @staticmethod
    def _set_if_not_none(var, key, value):
        if value is not None:
            var[key] = value

    @staticmethod
    def re_match(pattern, string, flags=0):
        return re.match(pattern, string, flags)

    @staticmethod
    def re_search(pattern, string, flags=0):
        return re.search(pattern, string, flags)

    @staticmethod
    def basename(_path) -> str:
        return basename(_path)

    def get_url(self):
        return self._params['url']

    def get_domain(self):
        domain_uri = self._params.get('domain_uri', None)
        if not domain_uri:
            self._params['domain_uri'] = re.search('(https?://[^/]+)', self._params['url']).group(1)

        return self._params['domain_uri']

    def get_current_chapter(self):
        return self._storage['chapters'][self._storage['current_chapter']]

    def get_current_file(self):
        return self._storage['files'][self._storage['current_file']]

    def quest_callback(self, variants: enumerate, title: str, select_type=0):  # 0 = single, 1 = multiple
        pass

    def files_progress_callback(self, max_val: int, current_val: int, need_reset=False):
        pass

    def logger_callback(self, *args):
        pass

    def get_referrer(self):
        return self.referrer if hasattr(self, 'referrer') else self.get_domain()


class Archive:

    def __init__(self):
        self.files = []

    def add_file(self, file):
        self.files.append(file)

    def set_files_list(self, files):
        self.files = files

    def make(self, dist, info_file=None):
        if not len(self.files):
            return
        make_dirs(dirname(dist))
        archive = ZipFile(dist, 'w', ZIP_DEFLATED)
        for file in self.files:
            if is_file(file):
                archive.write(file, basename(file))
        if info_file:
            archive.writestr('info.txt', info_file)
        archive.close()
        self._maked()

    def _maked(self):
        for file in self.files:
            unlink(file)


class Provider(BaseProvider, AbstractProvider, metaclass=ABCMeta):

    _image_params = {
        'crop': False,
        # 'crop': (left, upper, width, height)
        'offsets_crop': False,
        # 'crop': (left, upper, right, lower)
        'auto_crop': False,
        # 'auto_crop': {'max_crop_size': 40, 'auto_crop_factor': 150},
    }
    _volumes_count = 0

    def __init__(self):
        self.re = re
        self.json = json
        self._params['temp_directory'] = get_temp_path()

    def _image_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._image_params, 'crop', params.get('crop', None))
        self._set_if_not_none(self._image_params, 'auto_crop', params.get('auto_crop', None))

    def _downloading_params_parser(self, params):
        params = params if isinstance(params, dict) else {}
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))
        self._set_if_not_none(self._params, 'path_temp', params.get('path_temp', None))

    def process(self, url, downloading_params=None, image_params=None):  # Main method
        self._params['url'] = url
        self._downloading_params_parser(downloading_params)
        self._image_params_parser(image_params)

        self._storage['cookies'] = self.get_cookies()
        self._storage['manga_name'] = self.get_manga_name()
        self._storage['main_content'] = self.get_main_content()
        self._storage['chapters'] = self.get_chapters()

        self.loop_chapters()

    def set_quest_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'quest_callback', callback)

    def set_progress_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'files_progress_callback', callback)

    def set_logger_callback(self, callback: Callable):  # Required call from initiator (CLI, GUI)
        setattr(self, 'logger_callback', callback)

    def __call_files_progress_callback(self):
        if self.files_progress_callback:
            _max, _current = len(self._storage['files']), self._storage['current_file']
            self.files_progress_callback(_max, _current, _current < 1)

    def loop_chapters(self):
        volumes = self._storage['chapters']
        if isinstance(volumes, list) and len(volumes) > 0:
            for idx, __url in enumerate(volumes):
                self._storage['current_chapter'] = idx
                self._loop_callback_volumes()
                self._storage['files'] = self.get_files()
                self.loop_files()

    def loop_files(self):
        archive = Archive()
        files = self._storage['files']
        if isinstance(files, list) and len(files) > 0:
            for idx, __url in enumerate(files):
                self._storage['current_file'] = idx
                self.__call_files_progress_callback()
                self._loop_callback_files()
                file = self.save_file()

                archive.add_file(file)

            self.make_archive(archive)

    def save_file(self):
        _url = self.http().normalize_uri(self.get_current_file())
        filename = remove_file_query_params(basename(_url))
        _path = get_temp_path('{}_{}'.format(self._storage['current_file'], filename))

        if not is_file(_path):
            self.http().download_file(_url, _path)
        return _path

    def make_archive(self, archive: Archive):
        _path = remove_file_query_params(self.get_archive_name())

        if not _path:
            _path = str(self._storage['current_chapter'])
        _path = path_join(
            self._params.get('path_destination', 'Manga'),
            self.get_manga_name(),
            _path + '.zip'
        )
        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), __downloader_uri__, __version__)

        archive.make(_path, info)

    def html_fromstring(self, addr, selector: str = None, idx: int = None):
        return self.document_fromstring(self.http_get(addr), selector, idx)

    def http(self) -> Http:
        http_params = {
            'allow_webp': None,
            'referrer_url': self.get_referrer(),
            'user_agent': self._params.get('user_agent', None),
            'proxies': None,
            'site_cookies': None,
        }
        http = Http(**http_params)
        return http

    def http_get(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().get(url=url, headers=headers, cookies=cookies)

    def http_post(self, url: str, headers: dict = None, cookies: dict = None):
        return self.http().post(url=url, headers=headers, cookies=cookies)

    def image_auto_crop(self, src_path, dest_path=None):
        image = Image(src_path=src_path)
        if isinstance(self._image_params['auto_crop'], dict):
            for i in self._image_params['auto_crop']:
                image.params[i] = self._image_params['auto_crop'][i]
        image.crop_auto(dest_path=dest_path)

    def image_manual_crop(self, src_path, dest_path=None):  # sizes: (left, top, right, bottom)
        if isinstance(self._image_params['crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual(sizes=self._image_params['crop'], dest_path=dest_path)
        elif isinstance(self._image_params['offsets_crop'], tuple):
            image = Image(src_path=src_path)
            image.crop_manual_with_offsets(offsets=self._image_params['offsets_crop'], dest_path=dest_path)
