import json
import re
from abc import ABCMeta
from sys import stderr, exit

from .base_classes import (
    Abstract,
    Archive,
    Base,
    Callbacks,
    # TODO
    CloudFlareProtect,
    Static
)
from .fs import (
    get_temp_path,
    is_file,
    basename,
    remove_file_query_params,
    path_join,
    unlink,
    file_size,
)
from .http import MultiThreads
from .meta import __downloader_uri__
from .meta import __version__
from .info import Info


class Provider(Base, Abstract, Static, Callbacks, metaclass=ABCMeta):
    _volumes_count = 0
    _archive = None
    _zero_fill = False
    _with_manga_name = False
    _info = None
    _simulate = False
    _volume = None
    _show_chapter_info = False

    def __init__(self, info: Info = None):
        super().__init__()
        self.re = re
        self.json = json
        self._params['temp_directory'] = get_temp_path()
        self._info = info

    def _params_parser(self, params):
        # image params
        self._set_if_not_none(self._image_params, 'crop_blank', params.get('crop_blank', False))
        self._set_if_not_none(
            self._image_params, 'crop',
            (params.get('xt', 0),
             params.get('xr', 0),
             params.get('xb', 0),
             params.get('xl', 0)),
        )
        self._image_params['no_webp'] = params.get('no_webp', False)
        # downloading params
        self._set_if_not_none(self._params, 'destination', params.get('destination', None))
        self._zero_fill = params.get('zero_fill')
        self._with_manga_name = params.get('with_manga_name')
        self._simulate = params.get('simulate')
        self._show_chapter_info = params.get('show_current_chapter_info', False)

    def process(self, url, params=None):  # Main method
        self._params['url'] = url
        params = params if isinstance(params, dict) else {}
        self._params_parser(params)
        for i in params:
            self._params.setdefault(i, params[i])

        self.prepare_cookies()
        self._storage['manga_name'] = self.get_manga_name()
        self._storage['main_content'] = self.content
        self._storage['chapters'] = self._prepare_chapters(self.get_chapters())

        if not self._params.get('reverse_downloading', False):
            self._storage['chapters'] = self._storage['chapters'][::-1]

        self._storage['init_cookies'] = self._storage['cookies']
        self._info and self._info.set_ua(self.http().user_agent)

        self.loop_chapters()

    def _check_archive(self):
        # check
        _path = self.get_archive_path()
        not_allow_archive = not self._params.get('rewrite_exists_archives', False)

        return not_allow_archive and is_file(_path)

    def _download_chapter(self, idx, _min, _max):
        if idx < _min or (idx >= _max > 0) or self._check_archive():
            return
        if not self._simulate:
            try:
                self.before_download_chapter()
                self._storage['files'] = self.get_files()
                self.loop_files()
            except Exception as e:
                # Main debug here
                # raise e
                print([e], file=stderr)
                self._info.set_last_volume_error(e)

    def loop_chapters(self):
        volumes = self._storage['chapters']
        _min = self._params.get('skip_volumes', 0)
        _max = self._params.get('max_volumes', 0)
        if _max > 0 and _min > 0:
            _max += _min - 1
        for idx, __url in enumerate(volumes):
            self.chapter_id = idx
            self._info.add_volume(self.chapter_for_json(), self.get_archive_path())
            self._download_chapter(idx, _min, _max)

    def loop_files(self):
        if isinstance(self._storage['files'], list):
            if self._show_chapter_info:
                print('\n\nCurrent chapter url: %s\n' % (self.chapter,))
            if len(self._storage['files']) == 0:
                # see Std
                print('Error processing file: %s' % self.get_archive_name(), file=stderr)
                return
            self._archive = Archive()
            self._archive.not_change_files_extension = self._params.get('not_change_files_extension', False)
            self._archive.no_webp = self._image_params.get('no_webp', False)
            self._call_files_progress_callback()

            if self._params.get('one_thread', False):
                self._one_thread_save(self._storage['files'])

            else:
                self._multi_thread_save(self._storage['files'])

            self.make_archive()

    def _save_file_params_helper(self, url, idx):
        if url is None:
            _url = self.http().normalize_uri(self.get_current_file())
        else:
            _url = url
        _url = self.before_file_save(_url, idx)
        filename = remove_file_query_params(basename(_url))
        _path = self.remove_not_ascii(self._image_name(idx, filename))
        _path = get_temp_path(_path)
        return _path, idx, _url

    def save_file(self, idx=None, callback=None, url=None, in_arc_name=None):
        _path, idx, _url = self._save_file_params_helper(url, idx)

        if not is_file(_path) or file_size(_path) < 32:
            self.http().download_file(_url, _path, idx)
        self.after_file_save(_path, idx)
        self._archive.add_file(_path)

        callable(callback) and callback()

        return _path

    def get_archive_path(self):
        # see Std
        _path = remove_file_query_params(self.get_archive_name())
        _path = self.remove_not_ascii(_path)

        if not _path:
            _path = str(self.chapter_id)

        name = self._params.get('name', '')
        if not len(name):
            name = self._storage['manga_name']

        additional_data_name = ''
        if self.http().has_error:
            additional_data_name = '.ERROR'
            self.http().has_error = False

        return path_join(
            self._params.get('destination', 'Manga'),
            name,
            _path + '.%s%s' % (additional_data_name, self._archive_type())
        )\
            .replace('?', '_')\
            .replace('"', '_')\
            .replace('>', '_')\
            .replace('<', '_')\
            .replace('|', '_')  # Windows...

    def make_archive(self):
        _path = self.get_archive_path()

        info = 'Site: {}\nDownloader: {}\nVersion: {}'.format(self.get_url(), __downloader_uri__, __version__)

        # """
        # make book info
        # """
        # if self._params['cbz']:
        #     self._archive.add_book_info(self._arc_meta_info())

        self._archive.add_info(info)
        try:
            self._archive.make(_path)
        except OSError as e:
            print('')
            print(e)
            self.log(e, file=stderr)
            self._info.set_last_volume_error(str(e))
            unlink(_path)

    def html_fromstring(self, url, selector: str = None, idx: int = None):
        params = {}
        if isinstance(url, dict):
            params = url['params']
            url = url['url']
        return self.document_fromstring(self.http_get(url, **params), selector, idx)

    def _multi_thread_callback(self):
        self._call_files_progress_callback()
        self._storage['current_file'] += 1

    def _multi_thread_save(self, files):
        threading = MultiThreads()
        # hack
        self._storage['current_file'] = 0
        if self._params.get('no_multi_threads', False):
            threading.max_threads = 2
        for idx, url in enumerate(files):
            threading.add(self.save_file, (idx, self._multi_thread_callback, url))

        threading.start()

    def _one_thread_save(self, files):

        for idx, __url in enumerate(files):
            self._storage['current_file'] = idx
            self._call_files_progress_callback()
            self.save_file()
        _max = len(self._storage['files'])
        self.progress(_max, _max)

    def cf_protect(self, url):
        """
        WARNING! Thins function replace cookies!
        :param url: str
        :return:
        """
        cf = CloudFlareProtect()
        params = cf.run(url)
        if len(params):
            self.update_cookies(params[0])
            self.update_ua(params[1])
            self._params['cf-protect'] = True

    def update_ua(self, ua):
        self._storage['user_agent'] = ua
        self.http().user_agent = ua
        self._info and self._info.set_ua(ua)

    def update_cookies(self, cookies):
        for k in cookies:
            self._storage['cookies'][k] = cookies[k]
            self.http().cookies[k] = cookies[k]

    @property
    def content(self):
        content = self._storage.get('main_content', None)
        if content is None:
            content = self.get_main_content()
        return content
