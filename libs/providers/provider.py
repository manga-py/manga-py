import json
import re
from abc import ABCMeta

from libs.cli import __version__, __downloader_uri__
from libs.fs import (
    get_temp_path,
    is_file,
    basename,
    remove_file_query_params,
    path_join,
)
from libs.http import MultiThreads
from .base_provider import (
    AbstractProvider,
    Archive,
    BaseProvider,
    ChapterHelper,  # TODO
    CloudFlareProtect
)


class Provider(BaseProvider, AbstractProvider, metaclass=ABCMeta):

    _volumes_count = 0

    def __init__(self):
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

        self._storage['start_cookies'] = self._storage['cookies'] = self.get_cookies()
        self._storage['manga_name'] = self.get_manga_name()
        self._storage['main_content'] = self.get_main_content()
        self._storage['chapters'] = self.get_chapters()

        self.loop_chapters()

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

        print(len(self._storage['files']))
        if isinstance(self._storage['files'], list) and len(self._storage['files']) > 0:

            if self._params.get('no_multi_threads', False):
                self._one_thread_save(archive, self._storage['files'])

            else:
                self._multi_thread_save(archive, self._storage['files'])

            self.make_archive(archive)
            print('make archive')
        print('end loop files')

    def save_file(self, _url, _path):
        if not is_file(_path):
            self.http().download_file(_url, _path)
        return _path

    def make_archive(self, archive: Archive):
        _path = remove_file_query_params(self.get_archive_name())

        if not _path:
            _path = str(self._storage['current_chapter'])
        _path = path_join(
            self._params.get('path_destination', 'Manga'),
            self._params.get('name', self.get_manga_name()),
            _path + '.zip'
        )
        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), __downloader_uri__, __version__)

        archive.make(_path, info)

    def html_fromstring(self, addr, selector: str = None, idx: int = None):
        return self.document_fromstring(self.http_get(addr), selector, idx)

    def _multi_thread_callback(self):

        self._call_files_progress_callback()
        self._loop_callback_files()

        self._storage['current_file'] += 1

    def _multi_thread_save(self, archive, files):
        threading = MultiThreads()
        urls = []
        for idx, __url in enumerate(files):

            self._storage['current_file'] = idx

            _url = self.http().normalize_uri(self.get_current_file())
            filename = remove_file_query_params(basename(_url))
            _path = get_temp_path('{}_{}'.format(self._storage['current_file'], filename))

            urls.append([idx, _url, _path])
            archive.add_file(_path)

        # hack
        self._storage['current_file'] = 0
        for url in urls:
            threading.add(self.save_file, (url[1], url[2]))

        threading.start(self._multi_thread_callback)

    def _one_thread_save(self, archive, files):

        for idx, __url in enumerate(files):
            self._storage['current_file'] = idx
            self._call_files_progress_callback()
            self._loop_callback_files()

            _url = self.http().normalize_uri(self.get_current_file())
            filename = remove_file_query_params(basename(_url))
            _path = get_temp_path('{}_{}'.format(self._storage['current_file'], filename))

            file = self.save_file(_url, _path)

            archive.add_file(file)

    def cf_protect(self, url):
        cf = CloudFlareProtect()
        self._storage['cookies'] = cf.run(url)
        return self._storage['cookies']
