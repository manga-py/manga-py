import json
import re
from abc import ABCMeta

from .version import __downloader_uri__
from .fs import (
    get_temp_path,
    is_file,
    basename,
    remove_file_query_params,
    path_join,
)
from .http import MultiThreads
from .base_classes import (
    Abstract,
    Archive,
    Base,
    ChapterHelper,  # TODO
    CloudFlareProtect,
    Static
)
from .version import __version__


class Provider(Base, Abstract, Static, metaclass=ABCMeta):

    _volumes_count = 0
    _archive = None

    def __init__(self):
        super().__init__()
        self.re = re
        self.json = json
        self._params['temp_directory'] = get_temp_path()

    def _params_parser(self, params):
        # image params
        self._set_if_not_none(self._image_params, 'crop', params.get('crop', None))
        self._set_if_not_none(self._image_params, 'auto_crop', params.get('auto_crop', None))
        # downloading params
        self._set_if_not_none(self._params, 'path_destination', params.get('path_destination', None))
        self._set_if_not_none(self._params, 'path_temp', params.get('path_temp', None))

    def process(self, url, params=None):  # Main method
        self._params['url'] = url
        params = params if isinstance(params, dict) else {}
        self._params_parser(params)
        for i in params:
            self._params.setdefault(i, params[i])

        self.prepare_cookies()
        self._storage['manga_name'] = self.get_manga_name()
        self._storage['main_content'] = self.get_main_content()
        self._storage['chapters'] = self.get_chapters()[::-1]

        self._storage['init_cookies'] = self._storage['cookies']

        self.loop_chapters()

    def _check_archive(self):
        # check
        _path = self.get_archive_path()
        not_allow_archive = not self._params.get('rewrite_exists_archives', False)

        return not_allow_archive and is_file(_path)

    def loop_chapters(self):
        volumes = self._storage['chapters']
        if isinstance(volumes, list):
            for idx, __url in enumerate(volumes):
                self._storage['current_chapter'] = idx
                self._loop_callback_chapters()

                if self._check_archive():
                    continue

                self._storage['files'] = self.get_files()
                self.loop_files()

    def __add_file_to_archive(self):
        if self._params.get('no_multi_threads', False):
            self._one_thread_save(self._storage['files'])

        else:
            self._multi_thread_save(self._storage['files'])

    def loop_files(self):
        if isinstance(self._storage['files'], list) and len(self._storage['files']) > 0:
            self._archive = Archive()
            self.__add_file_to_archive()
            self.make_archive()

    def save_file(self, callback=None, url=None):
        if url is None:
            _url = self.http().normalize_uri(self.get_current_file())
        else:
            _url = url

        filename = remove_file_query_params(basename(_url))
        _path = get_temp_path('{:0>2}_{}'.format(self._storage['current_file'], filename))
        _path = self.remove_not_ascii(_path)

        if not is_file(_path):
            self._archive.add_file(self.remove_not_ascii(_path))
            self.http().download_file(_url, _path)
        callable(callback) and callback()
        return _path

    def get_archive_path(self):
        _path = remove_file_query_params(self.get_archive_name())
        _path = self.remove_not_ascii(_path)

        if not _path:
            _path = str(self._storage['current_chapter'])

        name = self._params.get('name', '')
        if not len(name):
            name = self._storage['manga_name']

        return path_join(
            self._params.get('path_destination', 'Manga'),
            name,
            _path + '.zip'
        )

    def make_archive(self):
        _path = self.get_archive_path()

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), __downloader_uri__, __version__)

        self._archive.make(_path, info)

    def html_fromstring(self, url, selector: str = None, idx: int = None):
        params = {}
        if isinstance(url, dict):
            params = url['params']
            url = url['url']
        return self.document_fromstring(self.http_get(url, **params), selector, idx)

    def _multi_thread_callback(self):

        self._call_files_progress_callback()
        self._loop_callback_files()

        self._storage['current_file'] += 1

    def _multi_thread_save(self, files):
        import time
        threading = MultiThreads()
        # hack
        self._storage['current_file'] = 0
        for url in files:
            threading.add(target=self.save_file, args=[self._multi_thread_callback])

        time.sleep(5)

        threading.start()
        self.logger_callback('')

    def _one_thread_save(self, files):

        for idx, __url in enumerate(files):
            self._storage['current_file'] = idx
            self._call_files_progress_callback()
            self._loop_callback_files()
            self.save_file()

    def cf_protect(self, url):
        """
        WARNING! Thins function replace cookies!
        :param url: str
        :return:
        """
        cf = CloudFlareProtect()
        params = cf.run(url)
        self._storage['cookies'] = params[0]
        self._storage['user_agent'] = params[1]
        self._params['cf-protect'] = True

    def _get_cover_from_content(self, selector):
        if self.get_storage_content():
            image = self.document_fromstring(self.get_storage_content(), selector)
            if image and len(image):
                self.http().normalize_uri(image[0].get('src'))
